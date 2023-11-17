import discord
from discord.ext import commands


class paginator_buttons(discord.ui.View):
    def __init__(
        self,
        timeout: int,
        current_page: int,
        executor: discord.User,
        pages: list[discord.Embed],
    ):
        super().__init__(timeout=timeout)

        self.current_page = current_page
        self.executor = executor
        self.pages = pages
        self.response = None

    async def on_timeout(self) -> None:
        for child in self.children:
            child.disabled = True

        await self.response.edit(view=self)

    @discord.ui.button(
        style=discord.ButtonStyle.blurple,
        emoji="⏪",
    )
    async def first_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.executor.id:
            return await interaction.response.send_message(
                "You cannot interact with this menu.", ephemeral=True
            )
        self.current_page = 0
        self.current_page_number.label = f"{self.current_page + 1}/{len(self.pages)}"
        await interaction.response.edit_message(
            embed=self.pages[self.current_page], view=self
        )

    @discord.ui.button(
        style=discord.ButtonStyle.blurple,
        emoji="⬅️",
    )
    async def previous_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.executor.id:
            return await interaction.response.send_message(
                "You cannot interact with this menu.", ephemeral=True
            )

        if self.current_page == 0:
            self.current_page = len(self.pages) - 1
            self.current_page_number.label = (
                f"{self.current_page + 1}/{len(self.pages)}"
            )
            return await interaction.response.edit_message(
                embed=self.pages[self.current_page], view=self
            )
        self.current_page -= 1
        self.current_page_number.label = f"{self.current_page + 1}/{len(self.pages)}"
        await interaction.response.edit_message(
            embed=self.pages[self.current_page], view=self
        )

    @discord.ui.button(
        label=f"page",
        style=discord.ButtonStyle.gray,
        disabled=True,
    )
    async def current_page_number(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.executor.id:
            return await interaction.response.send_message(
                "You cannot interact with this menu.", ephemeral=True
            )

        return

    @discord.ui.button(
        style=discord.ButtonStyle.blurple,
        emoji="➡️",
    )
    async def next_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.executor.id:
            return await interaction.response.send_message(
                "You cannot interact with this menu.", ephemeral=True
            )

        if len(self.pages) == self.current_page + 1:
            self.current_page = 0
            self.current_page_number.label = (
                f"{self.current_page + 1}/{len(self.pages)}"
            )
            return await interaction.response.edit_message(
                embed=self.pages[self.current_page - len(self.pages)], view=self
            )

        self.current_page += 1
        self.current_page_number.label = f"{self.current_page + 1}/{len(self.pages)}"
        await interaction.response.edit_message(
            embed=self.pages[self.current_page], view=self
        )

    @discord.ui.button(
        style=discord.ButtonStyle.blurple,
        emoji="⏩",
    )
    async def last_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.executor.id:
            return await interaction.response.send_message(
                "You cannot interact with this menu.", ephemeral=True
            )

        self.current_page = len(self.pages) - 1
        self.current_page_number.label = f"{self.current_page + 1}/{len(self.pages)}"
        await interaction.response.edit_message(
            embed=self.pages[self.current_page], view=self
        )


class Paginator:
    class Simple:
        def __init__(
            self, timeout: int = 60, initial_page: int = 0, ephemeral: bool = False
        ):
            self.timeout = timeout
            self.initial_page = initial_page
            self.ephemeral = ephemeral

        async def paginate(
            self,
            ctx: commands.Context | discord.Interaction,
            pages: list[discord.Embed],
        ):
            if isinstance(ctx, discord.Interaction):
                ctx = await commands.Context.from_interaction(ctx)

            view = paginator_buttons(self.timeout, self.initial_page, ctx.author, pages)
            view.current_page_number.label = f"{self.initial_page + 1}/{len(pages)}"

            view.response = await ctx.reply(
                embed=pages[self.initial_page],
                view=view,
                ephemeral=self.ephemeral,
            )
