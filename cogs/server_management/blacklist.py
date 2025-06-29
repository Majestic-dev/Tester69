import discord
from discord.ext import commands

from discord import app_commands

from utils import data_manager

class blacklist(commands.GroupCog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="add_words",
        description="Add words to the blacklisted words list",
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(
        blacklisted_words="The word(s) to add to the blacklisted words list, if adding multiple, separate them by commas (a, b)"
    )
    async def add_blacklisted_words(
        self, interaction: discord.Interaction, blacklisted_words: str
    ):
        await interaction.response.defer(ephemeral=True)
        filtered_words = await data_manager.get_filter_data(interaction.guild.id)
        old_existing_words = filtered_words["blacklisted_words"]
        new_existing_words = old_existing_words.copy()
        words_not_added = []

        for i in blacklisted_words.split(","):
            if i.strip() in old_existing_words:
                words_not_added.append(i.strip())
                pass
            elif i.strip() not in old_existing_words:
                new_existing_words.append(i.strip())

        await data_manager.edit_filter_data(
            interaction.guild.id, "blacklisted_words", new_existing_words
        )

        if len(words_not_added) >= 0 and (
            len(new_existing_words) > len(old_existing_words)
        ):
            return await interaction.edit_original_response(
                embed=discord.Embed(
                    description=(
                        f"<:white_checkmark:1096793014287995061> Added the following words to the blacklisted words list:\n\n"
                        f"`{', '.join(list(set(new_existing_words) - set(old_existing_words)))}`\n\n"
                    )
                    + (
                        f"Could not add the following words to the blacklisted words list because they already exist there:\n"
                        f"`{', '.join(words_not_added)}`"
                        if len(words_not_added) > 0
                        else ""
                    ),
                    colour=discord.Colour.green(),
                )
            )

        elif len(words_not_added) > 0 and (
            len(new_existing_words) == len(old_existing_words)
        ):
            return await interaction.edit_original_response(
                embed=discord.Embed(
                    description=f"<:white_cross:1096791282023669860> Could not add any of the words to the blacklisted words list because they already exist there!",
                    colour=discord.Colour.orange(),
                ),
            )

    async def word_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        filtered_words = await data_manager.get_filter_data(interaction.guild.id)
        words_in_blacklist = filtered_words["blacklisted_words"]

        return [
            app_commands.Choice(name=word, value=word)
            for word in words_in_blacklist
            if word.lower().startswith(current.lower()) or len(current) < 1
        ]

    @app_commands.command(
        name="remove_word",
        description="Remove a blacklisted word from the blacklisted words list.",
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.autocomplete(blacklisted_word=word_autocomplete)
    @app_commands.describe(
        blacklisted_word="The word to remove from the blacklisted words list"
    )
    async def remove_blacklisted_word(
        self, interaction: discord.Interaction, blacklisted_word: str
    ):
        filtered_words = await data_manager.get_filter_data(interaction.guild.id)
        blacklisted_words = filtered_words["blacklisted_words"]

        if (
            blacklisted_words is None
            or blacklisted_word.lower() not in blacklisted_words
        ):
            return await interaction.response.send_message(
                ephemeral=True,
                embed=discord.Embed(
                    description=f'<:white_cross:1096791282023669860> Could not remove "{blacklisted_word.lower()}" from blacklisted words list, because it does not exist there',
                    colour=discord.Colour.orange(),
                ),
            )

        elif blacklisted_word.lower() in blacklisted_words:
            blacklisted_words.remove(blacklisted_word.lower())
            await data_manager.edit_filter_data(
                interaction.guild.id, "blacklisted_words", blacklisted_words
            )
            return await interaction.response.send_message(
                ephemeral=True,
                embed=discord.Embed(
                    description=f'<:white_checkmark:1096793014287995061> Removed "{blacklisted_word.lower()}" from blacklisted words list',
                    colour=discord.Colour.green(),
                ),
            )

    @app_commands.command(
        name="list_words",
        description="List all blacklisted words in this server",
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    async def list_blacklisted_words(self, interaction: discord.Interaction):
        filtered_words = await data_manager.get_filter_data(interaction.guild.id)
        blacklisted_words = filtered_words["blacklisted_words"]

        if blacklisted_words is None or len(blacklisted_words) == 0:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description=f"<:white_cross:1096791282023669860> There are no blacklisted words in this server",
                    colour=discord.Colour.orange(),
                )
            )

        await interaction.response.send_message(
            embed=discord.Embed(
                description="Blacklisted words in this server:\n\n" + f"`{', '.join(blacklisted_words)}`",
                colour=discord.Colour.green(),
            ),
            ephemeral=True,
        )

async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(blacklist(bot))