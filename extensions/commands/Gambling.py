import json
import random

import discord
from discord import app_commands
from discord.ext import commands

from utils import DataManager


class Gambling(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="gamble", description="Gamble your set amount of coins")
    async def _gamble(self, interaction: discord.Interaction, bet: int = None):
        user_data = DataManager.get_user_data(interaction.user.id)

        if bet is None or bet < 0 or bet > 10000000:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Bet Failed",
                    description="You have to add a bet between 0 and 10000000, for example `'gamble 10`",
                    colour=discord.Colour.orange(),
                )
            )
            return

        if bet > 10000000:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Too High Bet",
                    description=(f"You cannot bet more than 10 million coins"),
                    colour=discord.Colour.orange(),
                )
            )

        if bet > user_data["balance"]:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="No Coins To Gamble",
                    description=(
                        f'You do not have enough funds to gamble. Your balance is {user_data["balance"]}'
                    ),
                    colour=discord.Colour.orange(),
                )
            )

        DataManager.edit_user_data(
            interaction.user.id, "balance", user_data["balance"] - bet
        )

        win = random.choices([True, False], [45, 55])[0]
        if win:
            multipliers = [
                1,
                1.1,
                1.2,
                1.3,
                1.4,
                1.5,
                1.6,
                1.7,
                1.8,
                1.9,
                2,
            ]
            chances = [11, 10, 10, 9, 8, 7, 6, 5, 4, 3, 2]
            multiplier = random.choices(multipliers, chances)[0]
            winnings = int(bet * multiplier)

            DataManager.edit_user_data(
                interaction.user.id, "balance", user_data["balance"] + winnings
            )

            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Bet Results",
                    description=(
                        f'Congratulations! You won {winnings - bet} and your new balance is {user_data["balance"] + winnings}'
                    ),
                    colour=discord.Colour.green(),
                )
            )

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Bet Results",
                description=(
                    f'Sorry, you lost {bet}. Your new balance is {user_data["balance"] - bet}'
                ),
                colour=discord.Colour.red(),
            )
        )

    @app_commands.command(
        name="snakeeyes",
        description="Gamble your coins in a snake eyes game for a chance to win big!",
    )
    async def snakeeyes(self, interaction: discord.Interaction, bet: int):
        user_data = DataManager.get_user_data(interaction.user.id)

        if bet > user_data["balance"]:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Not Enough Coins",
                    description="You do not have enough coins for that bet",
                    colour=discord.Colour.orange(),
                )
            )

        roll1 = random.randint(1, 6)
        roll2 = random.randint(1, 6)

        if roll1 == 1 and roll2 == 1:
            DataManager.edit_user_data(
                interaction.user.id, "balance", user_data["balance"] + 30 * bet
            )

            await interaction.response.send_message(
                embed=discord.Embed(
                    title="SNAKE EYES!",
                    description=(f"You rolled Snake Eyes! You won {30 * bet} coins!"),
                    colour=discord.Colour.green(),
                )
            )

        elif roll1 == 1 or roll2 == 1:
            DataManager.edit_user_data(
                interaction.user.id, "balance", user_data["balance"] + 1.5 * bet
            )

            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Snake Eye!",
                    description=(f"You rolled 1 snake eye! You won {1.5 * bet} coins!"),
                    colour=discord.Colour.green(),
                )
            )
        else:
            DataManager.edit_user_data(
                interaction.user.id, "balance", user_data["balance"] - bet
            )

            await interaction.response.send_message(
                embed=discord.Embed(
                    title="You lost",
                    description=(
                        f"You rolled a {roll1} and a {roll2}. You lost {bet} coins."
                    ),
                    colour=discord.Colour.orange(),
                )
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Gambling(bot))
