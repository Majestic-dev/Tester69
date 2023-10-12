import discord
from discord import app_commands
from discord.ext import commands

from utils import DataManager


class RoleDropdown(discord.ui.Select):
    def __init__(
        self,
        bot: commands.AutoShardedBot,
        interaction: discord.Interaction,
        guild: discord.Guild,
        message: discord.Message,
    ):
        self.bot = bot
        self.interaction = interaction
        self.guild = guild
        self.message = message

        options = [
            discord.SelectOption(label=f"{role.name}", value=f"{role.id}")
            for role in self.guild.roles.__reversed__()
        ]

        super().__init__(
            placeholder="Select the panel moderators",
            min_values=1,
            max_values=len(options[:25]),
            options=options[:25],
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        panel_data = await DataManager.get_panel_data(
            self.message.id, interaction.guild.id
        )
        await self.message.edit(
            embed=discord.Embed(
                title=f"{panel_data['panel_title']}",
                description=f"{panel_data['panel_description']}"
                + f"\n\nCurrent Panel Moderators: "
                + ",".join(
                    [
                        f"<@&{role.id}>"
                        for role in interaction.guild.roles
                        if role.id
                        in [int(value) for value in interaction.data["values"]]
                    ]
                ),
            )
        )

        await DataManager.edit_panel_moderators(
            self.message.id,
            interaction.guild.id,
            [int(value) for value in interaction.data["values"]],
        )


class RoleDropdownView(discord.ui.View):
    def __init__(
        self,
        bot: commands.AutoShardedBot,
        interaction: discord.Interaction,
        guild: discord.Guild,
        message: discord.Message,
    ):
        self.bot = bot
        self.interaction = interaction
        self.guild = guild

        super().__init__()

        self.add_item(
            RoleDropdown(
                bot=self.bot,
                interaction=self.interaction,
                guild=self.guild,
                message=message,
            )
        )


class ChannelDropdown(discord.ui.Select):
    def __init__(
        self,
        bot: commands.AutoShardedBot,
        interaction: discord.Interaction,
        message: discord.Message,
        category: discord.CategoryChannel,
    ):
        self.bot = bot
        self.interaction = interaction
        self.message = message
        self.category = category

        options = [
            discord.SelectOption(label=f"{channel.name}", value=f"{channel.id}")
            for channel in self.category.channels
            if channel.type == discord.ChannelType.text
        ]

        super().__init__(
            placeholder="Select where to send the panel",
            min_values=1,
            max_values=1,
            options=options[:25],
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        panel_data = await DataManager.get_panel_data(
            self.interaction.message.id, interaction.guild.id
        )
        channel = self.interaction.guild.get_channel(int(interaction.data["values"][0]))
        await channel.send(
            embed=discord.Embed(
                title=f"{panel_data['panel_title']}",
                description=f"{panel_data['panel_description']}",
                color=discord.Color.blurple(),
            ),
            view=PanelViews(self.bot, self.message.id),
        )


class ChannelDropdownView(discord.ui.View):
    def __init__(
        self,
        bot: commands.AutoShardedBot,
        interaction: discord.Interaction,
        message: discord.Message,
        category: discord.CategoryChannel,
    ):
        self.bot = bot
        self.interaction = interaction
        self.message = message
        self.category = category

        super().__init__()

        self.add_item(
            ChannelDropdown(
                bot=self.bot,
                interaction=self.interaction,
                message=self.message,
                category=self.category,
            )
        )


class PanelEditModal(discord.ui.Modal, title="Edit Panel"):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    panelTitle = discord.ui.TextInput(
        label="Title of the panel",
        style=discord.TextStyle.short,
        max_length=50,
    )

    panelDescription = discord.ui.TextInput(
        label="Description of the panel",
        style=discord.TextStyle.short,
        max_length=100,
    )

    limitPerUser = discord.ui.TextInput(
        label="Limit per user",
        style=discord.TextStyle.short,
        required=False,
        max_length=3,
    )

    async def on_submit(self, interaction: discord.Interaction):
        if self.limitPerUser.value.isnumeric():
            await interaction.response.defer()
            message = await interaction.original_response()
            panel_data = await DataManager.get_panel_data(
                message.id, interaction.guild.id
            )
            panel_moderators = [
                f"<@&{role_id}>" for role_id in panel_data["panel_moderators"]
            ]
            await interaction.edit_original_response(
                embed=discord.Embed(
                    title=self.panelTitle.value,
                    description=f"{self.panelDescription.value}"
                    + (
                        f"\n\nCurrent Panel Moderators: {','.join(panel_moderators)}"
                        if panel_moderators
                        else ""
                    ),
                )
            )
            await DataManager.edit_panel(
                message.id, interaction.guild.id, "panel_title", self.panelTitle.value
            )
            await DataManager.edit_panel(
                message.id,
                interaction.guild.id,
                "panel_description",
                self.panelDescription.value,
            )
            await DataManager.edit_panel(
                message.id,
                interaction.guild.id,
                "limit_per_user",
                int(self.limitPerUser.value),
            )
        else:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error",
                    description="Limit per user must be a number",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )


class TicketCreateModal(discord.ui.Modal, title="Create a Ticket"):
    def __init__(self, bot, panel_id) -> None:
        super().__init__()
        self.bot = bot
        self.panel_id = panel_id

    ticketReason = discord.ui.TextInput(
        label="Reason for creating a ticket",
        style=discord.TextStyle.short,
        max_length=100,
    )

    detailedReason = discord.ui.TextInput(
        label="Detailed reason for creating a ticket",
        style=discord.TextStyle.short,
        required=False,
        max_length=500,
    )

    async def on_submit(self, interaction: discord.Interaction):
        panel_data = await DataManager.get_panel_data(
            self.panel_id, interaction.guild.id
        )
        ticket = await interaction.channel.create_thread(
            name=f"ticket-{interaction.user.name}",
        )
        await DataManager.create_ticket(
            self.panel_id, interaction.guild.id, ticket.id, interaction.user.id
        )
        await ticket.add_user(interaction.user)

        await interaction.response.send_message(
            f"Your ticket has been created in {ticket.mention}", ephemeral=True
        )
        ticket_moderators = [
            f"<@&{role_id}>" for role_id in panel_data["panel_moderators"]
        ]
        message = await ticket.send(
            content=f"{','.join(ticket_moderators)}, {interaction.user.mention}",
            embed=discord.Embed(
                title=self.ticketReason.value,
                description=self.detailedReason.value,
                color=discord.Color.blurple(),
            ),
            view=TicketViews(self.bot, self.panel_id, interaction.user.id),
        )
        await message.pin()


class ClosedTicketViews(discord.ui.View):
    def __init__(self, bot, panel_id, user_id):
        super().__init__(timeout=None)
        self.bot = bot
        self.panel_id = panel_id
        self.user_id = user_id

    @discord.ui.button(
        label="Reopen Ticket",
        style=discord.ButtonStyle.green,
        custom_id="ticket:reopen_ticket",
        emoji="🔓",
    )
    async def reopen_ticket(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer(ephemeral=True)
        ticket = await DataManager.get_ticket(interaction.channel.id)
        await DataManager.open_ticket(self.panel_id, interaction.channel.id)
        user = self.bot.get_user(self.user_id)
        await interaction.delete_original_response()
        await interaction.channel.add_user(user)
        await interaction.channel.send(
            embed=discord.Embed(
                title="Ticket Reopened",
                description=f"Ticket reopened by {interaction.user.mention}",
                color=discord.Color.green(),
            )
        )

    @discord.ui.button(
        label="Delete Ticket",
        style=discord.ButtonStyle.red,
        custom_id="ticket:delete_ticket",
        emoji="🗑️",
    )
    async def delete_ticket(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer(ephemeral=True)
        await interaction.channel.delete()


class TicketViews(discord.ui.View):
    def __init__(self, bot, panel_id, user_id):
        super().__init__(timeout=None)
        self.bot = bot
        self.panel_id = panel_id
        self.user_id = user_id

    @discord.ui.button(
        label="Close Ticket",
        style=discord.ButtonStyle.red,
        custom_id="ticket:close_ticket",
        emoji="🔒",
    )
    async def close_ticket(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        ticket = await DataManager.get_ticket(interaction.channel.id)
        if ticket["closed"] == True:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Ticket Already Closed!",
                    description="This ticket has already been closed",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )

        elif ticket["closed"] == False:
            await DataManager.close_ticket(self.panel_id, interaction.channel.id)
            panel_data = await DataManager.get_panel_data(
                self.panel_id, interaction.guild.id
            )
            for user in await interaction.channel.fetch_members():
                member = interaction.guild.get_member(user.id)
                if any(
                    role.id in panel_data["panel_moderators"] for role in member.roles
                ):
                    continue
                else:
                    await interaction.channel.remove_user(member)

            user = self.bot.get_user(self.user_id)
            await interaction.channel.remove_user(user)
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Ticket Closed",
                    description=f"Ticket closed by {interaction.user.mention}",
                    color=discord.Color.red(),
                ),
                view=ClosedTicketViews(self.bot, self.panel_id, self.user_id),
            )


class PanelViews(discord.ui.View):
    def __init__(self, bot, panel_id):
        super().__init__(timeout=None)
        self.bot = bot
        self.panel_id = panel_id

    @discord.ui.button(
        label="Create Ticket",
        style=discord.ButtonStyle.green,
        custom_id="ticket:create_ticket",
        emoji="📩",
    )
    async def create_ticket(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        panel_data = await DataManager.get_panel_data(
            self.panel_id, interaction.guild.id
        )
        i = 0
        for thread in interaction.channel.threads:
            if thread.name == f"ticket-{interaction.user.name}":
                try:
                    await thread.fetch_member(interaction.user.id)
                    i += 1
                except discord.errors.NotFound:
                    continue

        if i >= panel_data["limit_per_user"]:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Too Many Tickets Opened",
                    description="You already have the maximum amount of tickets open, please close the other tickets before creating a new one",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )

        await interaction.response.send_modal(
            TicketCreateModal(self.bot, self.panel_id)
        )


class PanelCreationViews(discord.ui.View):
    def __init__(self, bot, executor_id):
        super().__init__()
        self.bot = bot
        self.executor_id = executor_id

    @discord.ui.button(
        label="Edit Panel Moderators",
        style=discord.ButtonStyle.blurple,
        custom_id="panel:add_moderators",
        emoji="👮",
    )
    async def add_moderators(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.executor_id:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error",
                    description="You are not the executor of this panel",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        await interaction.response.send_message(
            view=RoleDropdownView(
                bot=self.bot,
                interaction=interaction,
                guild=interaction.guild,
                message=interaction.message,
            ),
            ephemeral=True,
        )

    @discord.ui.button(
        label="Edit Panel",
        style=discord.ButtonStyle.blurple,
        custom_id="panel:edit_panel",
        emoji="📝",
    )
    async def edit_panel(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.executor_id:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error",
                    description="You are not the executor of this panel",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        await interaction.response.send_modal(PanelEditModal(self.bot))

    @discord.ui.button(
        label="Delete Panel",
        style=discord.ButtonStyle.red,
        custom_id="panel:delete_panel",
        emoji="🗑️",
    )
    async def delete_panel(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.executor_id:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error",
                    description="You are not the executor of this panel",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        await interaction.response.defer(ephemeral=True)
        await DataManager.delete_panel(interaction.message.id, interaction.guild.id)
        await interaction.message.delete()

    @discord.ui.button(
        label="Submit Panel",
        style=discord.ButtonStyle.green,
        custom_id="panel:submit_panel",
        emoji="✅",
    )
    async def submit_panel(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.executor_id:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error",
                    description="You are not the executor of this panel",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        panel_data = await DataManager.get_panel_data(
            interaction.message.id, interaction.guild.id
        )
        if panel_data["panel_moderators"]:
            await interaction.message.delete()
            await interaction.response.send_message(
                view=ChannelDropdownView(
                    bot=self.bot,
                    interaction=interaction,
                    message=interaction.message,
                    category=interaction.channel.category,
                ),
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Panel Moderators",
                    description="You need to set the panel moderators before submitting the panel",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )


class Ticket(commands.GroupCog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="create_panel", description="Create a ticket panel in the current category"
    )
    async def ticket(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Ticket Panel Creation",
                description="Create a ticket panel",
                color=discord.Color.blurple(),
            ),
            view=PanelCreationViews(self.bot, interaction.user.id),
        )
        message = await interaction.original_response()

        await DataManager.create_panel(
            message.id,
            interaction.guild.id,
            1,
            "Ticket Panel",
            "Ticket Panel Decsription",
            [],
        )


async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(Ticket(bot))
