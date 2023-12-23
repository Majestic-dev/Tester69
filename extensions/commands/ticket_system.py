import discord
from discord import app_commands
from discord.ext import commands

from utils import DataManager


class create_role_dropdown(discord.ui.RoleSelect):
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

        super().__init__(
            placeholder="Select the panel moderators",
            min_values=1,
            max_values=len(guild.roles),
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
                colour=discord.Colour.blurple(),
            )
        )

        await DataManager.edit_panel_moderators(
            self.message.id,
            interaction.guild.id,
            [int(value) for value in interaction.data["values"]],
        )


class edit_role_dropdown(discord.ui.RoleSelect):
    def __init__(
        self,
        bot: commands.AutoShardedBot,
        panel_id: int,
        interaction: discord.Interaction,
        paneledit,
    ):
        self.bot = bot
        self.panel_id = panel_id
        self.interaction = interaction
        self.paneledit = paneledit

        super().__init__(
            placeholder="Select the panel moderators",
            min_values=1,
            max_values=len(self.interaction.guild.roles),
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        panel_data = await DataManager.get_panel_data(
            self.panel_id, interaction.guild.id
        )
        await self.interaction.edit_original_response(
            embed=discord.Embed(
                title=self.paneledit.panel_title,
                description=self.paneledit.panel_description
                + f"\n\nCurrent Panel Moderators: "
                + ",".join(
                    [
                        f"<@&{role.id}>"
                        for role in interaction.guild.roles
                        if role.id
                        in [int(value) for value in interaction.data["values"]]
                    ]
                ),
                colour=discord.Colour.blurple(),
            )
        )

        self.paneledit.panel_moderators = [
            int(value) for value in interaction.data["values"]
        ]


class create_role_dropdown_view(discord.ui.View):
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
            create_role_dropdown(
                bot=self.bot,
                interaction=self.interaction,
                guild=self.guild,
                message=message,
            )
        )


class edit_role_dropdown_view(discord.ui.View):
    def __init__(
        self,
        bot: commands.AutoShardedBot,
        panel_id: int,
        interaction: discord.Interaction,
        paneledit,
    ):
        self.bot = bot
        self.panel_id = panel_id
        self.interaction = interaction
        self.paneledit = paneledit

        super().__init__()

        self.add_item(
            edit_role_dropdown(
                bot=self.bot,
                panel_id=self.panel_id,
                interaction=self.interaction,
                paneledit=self.paneledit,
            )
        )


class channel_dropdown(discord.ui.ChannelSelect):
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

        super().__init__(
            channel_types=[discord.ChannelType.text],
            placeholder="Select where to send the panel",
            min_values=1,
            max_values=1,
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        panel_data = await DataManager.get_panel_data(
            self.interaction.message.id, interaction.guild.id
        )
        channel = self.interaction.guild.get_channel(int(interaction.data["values"][0]))
        panel = await channel.send(
            embed=discord.Embed(
                title=f"{panel_data['panel_title']}",
                description=f"{panel_data['panel_description']}",
                colour=discord.Colour.blurple(),
            )
        )

        await panel.edit(view=panel_views(self.bot, panel.id))
        await DataManager.edit_panel(
            self.message.id, interaction.guild.id, "id", panel.id
        )


class channel_dropdown_view(discord.ui.View):
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
            channel_dropdown(
                bot=self.bot,
                interaction=self.interaction,
                message=self.message,
                category=self.category,
            )
        )


class create_panel_edit_modal(discord.ui.Modal, title="Edit Panel"):
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
        default=1,
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
                    description=self.panelDescription.value
                    + (
                        f"\n\nCurrent Panel Moderators: {','.join(panel_moderators)}"
                        if panel_moderators
                        else ""
                    ),
                    colour=discord.Colour.blurple(),
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
                    colour=discord.Colour.red(),
                ),
                ephemeral=True,
            )


class edit_panel_edit_modal(discord.ui.Modal, title="Edit Panel"):
    def __init__(self, bot, interaction, panel_id, paneledit) -> None:
        super().__init__()
        self.bot = bot
        self.interaction = interaction
        self.panel_id = panel_id
        self.paneledit = paneledit

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
        default=1,
        max_length=3,
    )

    async def on_submit(self, interaction: discord.Interaction):
        if self.limitPerUser.value.isnumeric():
            await interaction.response.defer()
            panel_moderators = [
                f"<@&{role_id}>" for role_id in self.paneledit.panel_moderators
            ]
            await self.interaction.edit_original_response(
                embed=discord.Embed(
                    title=self.panelTitle.value,
                    description=self.panelDescription.value
                    + (
                        f"\n\nCurrent Panel Moderators: {','.join(panel_moderators)}"
                        if panel_moderators
                        else ""
                    ),
                    colour=discord.Colour.blurple(),
                )
            )
            self.paneledit.panel_title = self.panelTitle.value
            self.paneledit.panel_description = self.panelDescription.value
            self.paneledit.limit_per_user = int(self.limitPerUser.value)

        else:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error",
                    description="Limit per user must be a number",
                    colour=discord.Colour.red(),
                ),
                ephemeral=True,
            )


class create_ticket_modal(discord.ui.Modal, title="Create a Ticket"):
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
                colour=discord.Colour.blurple(),
            ),
            view=ticket_views(self.bot, self.panel_id, interaction.user.id),
        )
        await message.pin()


class closed_ticket_views(discord.ui.View):
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
                colour=discord.Colour.green(),
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


class ticket_views(discord.ui.View):
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
                    colour=discord.Colour.red(),
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
                    colour=discord.Colour.red(),
                ),
                view=closed_ticket_views(self.bot, self.panel_id, self.user_id),
            )


class panel_views(discord.ui.View):
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
                    colour=discord.Colour.red(),
                ),
                ephemeral=True,
            )

        await interaction.response.send_modal(
            create_ticket_modal(self.bot, self.panel_id)
        )


class panel_creation_views(discord.ui.View):
    def __init__(self, bot, executor_id):
        super().__init__()
        self.bot = bot
        self.executor_id = executor_id

    @discord.ui.button(
        label="Edit Panel Moderators",
        style=discord.ButtonStyle.blurple,
        custom_id="panel:add_moderators",
        emoji="👮",
        row=1,
    )
    async def add_moderators(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.executor_id:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error",
                    description="You are not the executor of this panel",
                    colour=discord.Colour.red(),
                ),
                ephemeral=True,
            )
        await interaction.response.send_message(
            view=create_role_dropdown_view(
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
        row=1,
    )
    async def edit_panel(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.executor_id:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error",
                    description="You are not the executor of this panel",
                    colour=discord.Colour.red(),
                ),
                ephemeral=True,
            )
        await interaction.response.send_modal(create_panel_edit_modal(self.bot))

    @discord.ui.button(
        label="Delete Panel",
        style=discord.ButtonStyle.red,
        custom_id="panel:delete_panel",
        emoji="🗑️",
        row=2,
    )
    async def delete_panel(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.executor_id:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error",
                    description="You are not the executor of this panel",
                    colour=discord.Colour.red(),
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
        row=2,
    )
    async def submit_panel(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.executor_id:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error",
                    description="You are not the executor of this panel",
                    colour=discord.Colour.red(),
                ),
                ephemeral=True,
            )
        panel_data = await DataManager.get_panel_data(
            interaction.message.id, interaction.guild.id
        )
        if panel_data["panel_moderators"]:
            await interaction.message.delete()
            await interaction.response.send_message(
                view=channel_dropdown_view(
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
                    colour=discord.Colour.red(),
                ),
                ephemeral=True,
            )


class panel_edit_views(discord.ui.View):
    def __init__(
        self,
        bot,
        panel_id,
        interaction,
        panel_title,
        panel_description,
        limit_per_user,
        panel_moderators,
    ):
        super().__init__()
        self.bot = bot
        self.panel_id = panel_id
        self.interaction = interaction
        self.panel_title = panel_title
        self.panel_description = panel_description
        self.limit_per_user = limit_per_user
        self.panel_moderators = panel_moderators

    @discord.ui.button(
        label="Edit Panel Moderators",
        style=discord.ButtonStyle.blurple,
        custom_id="panel:add_moderators",
        emoji="👮",
        row=1,
    )
    async def add_moderators(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        await interaction.response.send_message(
            view=edit_role_dropdown_view(
                bot=self.bot,
                panel_id=self.panel_id,
                interaction=self.interaction,
                paneledit=self,
            ),
            ephemeral=True,
        )

    @discord.ui.button(
        label="Edit Panel",
        style=discord.ButtonStyle.blurple,
        custom_id="panel:edit_panel",
        emoji="📝",
        row=1,
    )
    async def edit_panel(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_modal(
            edit_panel_edit_modal(self.bot, self.interaction, self.panel_id, self)
        )

    @discord.ui.button(
        label="Delete Panel",
        style=discord.ButtonStyle.red,
        custom_id="panel:delete_panel",
        emoji="🗑️",
        row=2,
    )
    async def delete_panel(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await DataManager.delete_panel(self.panel_id, interaction.guild.id)
        channel = self.bot.get_channel(interaction.channel.id)
        message = await channel.fetch_message(self.panel_id)
        await message.delete()
        await self.interaction.delete_original_response()

    @discord.ui.button(
        label="Submit Panel",
        style=discord.ButtonStyle.green,
        custom_id="panel:submit_panel",
        emoji="✅",
        row=2,
    )
    async def submit_panel(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        panel_data = await DataManager.get_panel_data(
            self.panel_id, interaction.guild.id
        )
        channel = self.bot.get_channel(interaction.channel.id)
        message = await channel.fetch_message(self.panel_id)
        await DataManager.edit_panel(
            self.panel_id, interaction.guild.id, "panel_title", self.panel_title
        )
        await DataManager.edit_panel(
            self.panel_id,
            interaction.guild.id,
            "panel_description",
            self.panel_description,
        )
        await DataManager.edit_panel(
            self.panel_id,
            interaction.guild.id,
            "limit_per_user",
            self.limit_per_user,
        )
        await DataManager.edit_panel_moderators(
            self.panel_id,
            interaction.guild.id, 
            self.panel_moderators,
        )
        if panel_data["panel_moderators"]: 
            await self.interaction.delete_original_response()
            await message.edit(
                embed=discord.Embed(
                    title=panel_data["panel_title"], 
                    description=panel_data["panel_description"], 
                    colour=discord.Colour.blurple(),
                ),
                view=panel_views(self.bot, self.panel_id),
            )
        else:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Panel Moderators",
                    description="You need to set the panel moderators before submitting the panel",
                    colour=discord.Colour.red(),
                ),
                ephemeral=True,
            )


class ticket(commands.GroupCog):
    def __init__(self, bot):
        self.bot = bot
        self.ctx_menu = app_commands.ContextMenu(
            name="Edit Panel",
            callback=self.edit_panel,
        )
        self.bot.tree.add_command(self.ctx_menu)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(self.ctx_menu.name, type=self.ctx_menu.type)

    @app_commands.command(
        name="create_panel", description="Create a ticket panel in the current category"
    )
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_channels=True)
    @app_commands.checks.cooldown(1, 30, key=lambda i: (i.guild.id)) 
    async def ticket(self, interaction: discord.Interaction, panel_title: str, panel_description: str):
        await interaction.response.send_message(
            embed=discord.Embed(
                title=panel_title,
                description=panel_description,
                colour=discord.Colour.blurple(),
            ),
            view=panel_creation_views(self.bot, interaction.user.id),
        )
        message = await interaction.original_response()

        await DataManager.create_panel(
            message.id,
            interaction.guild.id, 
            1,
            panel_title,
            panel_description,
            [],
        )

    @app_commands.guild_only()
    @app_commands.default_permissions(manage_channels=True)
    @app_commands.checks.cooldown(1, 30, key=lambda i: (i.guild.id)) 
    async def edit_panel(
        self, interaction: discord.Interaction, message: discord.Message
    ):
        if message.id in await DataManager.get_all_panel_ids(): 
            panel = await DataManager.get_panel_data(message.id, interaction.guild.id) 
            await interaction.response.send_message(
                embed=discord.Embed(
                    title=panel["panel_title"], 
                    description=panel["panel_description"] 
                    + (
                        f"\n\nCurrent Panel Moderators: {','.join([f'<@&{role_id}>' for role_id in panel['panel_moderators']])}" 
                        if panel["panel_moderators"] 
                        else ""
                    ),
                    colour=discord.Colour.blurple(),
                ),
                ephemeral=True,
                view=panel_edit_views(
                    self.bot,
                    message.id,
                    interaction,
                    panel["panel_title"], 
                    panel["panel_description"], 
                    panel["limit_per_user"], 
                    panel["panel_moderators"], 
                ),
            )
        else:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error",
                    description="This is not a ticket panel",
                    colour=discord.Colour.red(),
                ),
                ephemeral=True,
            )


async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(ticket(bot))
