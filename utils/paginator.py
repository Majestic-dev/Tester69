import discord


class PaginationButtons(discord.ui.View):
    def __init__(self, pages: list[discord.Embed], current_page: int):
        super().__init__()
        self.pages = pages
        self.current_page = current_page

    @discord.ui.button(
        style=discord.ButtonStyle.blurple,
        custom_id="persistent_view:first_page",
        emoji="⏪",
    )
    async def first_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.current_page = 0
        self.current_page_number.label = f"{self.current_page + 1}/{len(self.pages)}"
        await interaction.response.edit_message(
            embed=self.pages[self.current_page], view=self
        )

    @discord.ui.button(
        style=discord.ButtonStyle.blurple,
        custom_id="persistent_view:previous_page",
        emoji="⬅️",
    )
    async def previous_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
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
        style=discord.ButtonStyle.blurple,
        disabled=True,
    )
    async def current_page_number(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        return

    @discord.ui.button(
        style=discord.ButtonStyle.blurple,
        custom_id="persistent_view:next_page",
        emoji="➡️",
    )
    async def next_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
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
        custom_id="persistent_view:last_page",
        emoji="⏩",
    )
    async def last_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.current_page = len(self.pages) - 1
        self.current_page_number.label = f"{self.current_page + 1}/{len(self.pages)}"
        await interaction.response.edit_message(
            embed=self.pages[self.current_page], view=self
        )


class Paginator:
    class Simple:
        def __init__(
            self, initial_page: int = 0, ephemeral: bool = False
        ):
            self.initial_page = initial_page
            self.ephemeral = ephemeral

        async def start(
            self, interaction: discord.Interaction, pages: list[discord.Embed]
        ):
            view = PaginationButtons(pages, self.initial_page)
            try:
                view.current_page_number.label = f"{self.initial_page + 1}/{len(pages)}"
                await interaction.response.send_message(
                    embed=pages[self.initial_page], view=view, ephemeral=self.ephemeral
                )
            except discord.errors.InteractionResponded:
                view.current_page_number.label = f"{self.initial_page + 1}/{len(pages)}"
                await interaction.edit_original_response(
                    embed=pages[self.initial_page], view=view
                )
