import discord
from discord.ext import commands

class jump_to_page_modal(discord.ui.Modal, title="Jump to page"):
    def __init__(self, timeout: int, pages: list[discord.Embed], message: discord.Message) -> None:
        super().__init__()
        self.timeout = timeout
        self.pages = pages
        self.message = message

    async def check_pages(
        self, interaction: discord.Interaction, page_number: int
    ) -> bool:
        if page_number > len(self.pages) or page_number < 1:
            await interaction.response.send_message(
                "That page number is invalid.", ephemeral=True
            )
            return False
        return True
    
    page_number = discord.ui.TextInput(
        label="Enter a page number",
        style=discord.TextStyle.short,
        default="1",
        min_length=1,
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        if await self.check_pages(interaction, int(self.page_number.value)):
            view=paginator_buttons(self.timeout, int(self.page_number.value) - 1, interaction.user, self.pages)
            view.current_page_number.label = f"{int(self.page_number.value)}/{len(self.pages)}"
            await self.message.edit(
                embed=self.pages[int(self.page_number.value) - 1], view=view
            )
            await interaction.response.defer()

class on_page_counter_click(discord.ui.View):
    def __init__(
        self,
        executor: discord.User,
        pages: list[discord.Embed],
        original_message: discord.Message,
        interaction: discord.Interaction,
        message: discord.Message
    ):
        super().__init__()

        self.executor = executor
        self.pages = pages
        self.original_message = original_message
        self.interaction = interaction
        self.message = message

    @discord.ui.button(
        label="Stop Pagination",
        style=discord.ButtonStyle.red,
    )
    async def stop_pagination(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):  
        self.stop_pagination.disabled = True
        self.jump_to_page.disabled = True

        await self.original_message.edit(
            view=None
        )
        await interaction.response.defer()
        await self.interaction.edit_original_response(
            view=self
        )
    @discord.ui.button(
        label="Jump to page",
        style=discord.ButtonStyle.gray,
    )
    async def jump_to_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):  
        await interaction.response.send_modal(
            jump_to_page_modal(self.timeout, self.pages, self.message)
        )

class paginator_buttons(discord.ui.View):
    def __init__(
        self,
        timeout: int,
        current_page: int,
        executor: discord.User,
        pages: list[discord.Embed],
    ):
        super().__init__(timeout=timeout)

        self.timeout = timeout
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
    )
    async def current_page_number(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.executor.id:
            return await interaction.response.send_message(
                "You cannot interact with this menu.", ephemeral=True
            )
        
        await interaction.response.send_message(
            view=on_page_counter_click(self.executor, self.pages, interaction.message, interaction, self.response),
            ephemeral=True
        )

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
