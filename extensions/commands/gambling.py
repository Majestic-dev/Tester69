import asyncio
import random

import discord
from discord import app_commands
from discord.ext import commands

from utils import DataManager


class Gambling(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @app_commands.command(
        name="coinflip", description="Bet your 🪙 in a game of coinflip"
    )
    @app_commands.checks.cooldown(1, 25, key=lambda i: (i.user.id))
    @app_commands.choices(
        choices=[
            app_commands.Choice(name="Heads", value="heads"),
            app_commands.Choice(name="Tails", value="tails"),
        ]
    )
    @app_commands.describe(
        bet="The amount of 🪙 you want to bet", choices="Choose heads or tails"
    )
    async def coinflip(
        self,
        interaction: discord.Interaction,
        bet: int,
        choices: app_commands.Choice[str],
    ):
        user_data = await DataManager.get_user_data(interaction.user.id)

        if bet > user_data["balance"]:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You do not have enough 🪙 for that bet",
                    colour=discord.Colour.orange(),
                )
            )

        await DataManager.edit_user_data(
            interaction.user.id, "balance", user_data["balance"] - bet
        )

        result = random.choices(("heads", "tails"))[0]

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Flipping A Coin!",
                description="Flipping a coin <a:coinflip:1088886954713694398>",
                colour=discord.Colour.green(),
            )
        )
        await asyncio.sleep(3)

        if choices.value != result:
            return await interaction.edit_original_response(
                embed=discord.Embed(
                    title="You Lose!",
                    description=f"The coin landed on {result}, you lose {bet} 🪙!",
                    colour=discord.Colour.red(),
                )
            )

        await DataManager.edit_user_data(
            interaction.user.id, "balance", user_data["balance"] + bet * 2
        )

        await interaction.edit_original_response(
            embed=discord.Embed(
                title="You Won!",
                description=f"The coin landed on {result}, you win {bet} 🪙!",
                colour=discord.Colour.green(),
            )
        )

    @app_commands.command(name="gamble", description="Gamble your set amount of 🪙")
    @app_commands.checks.cooldown(1, 25, key=lambda i: (i.user.id))
    @app_commands.describe(bet="The amount of 🪙 you want to bet")
    async def gamble(self, interaction: discord.Interaction, bet: int):
        user_data = await DataManager.get_user_data(interaction.user.id)

        if bet > user_data["balance"]:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description=(
                        f"<:white_cross:1096791282023669860> You do not have enough 🪙 for that bet"
                    ),
                    colour=discord.Colour.orange(),
                )
            )

        await DataManager.edit_user_data(
            interaction.user.id, "balance", user_data["balance"] - bet
        )

        win = random.choices([True, False])[0]
        random1 = round(random.uniform(1.0, 3.0), 1)
        winnings = round(bet * random1, 0)
        if win == True:
            await DataManager.edit_user_data(
                interaction.user.id, "balance", user_data["balance"] + int(winnings)
            )
            user_data = await DataManager.get_user_data(interaction.user.id)

            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Bet Results",
                    description=(
                        f'Congratulations! You won {int(winnings)} 🪙 and your new balance is {user_data["balance"]} 🪙'
                    ),
                    colour=discord.Colour.green(),
                )
            )
        else:
            user_data = await DataManager.get_user_data(interaction.user.id)
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Bet Results",
                    description=(
                        f'Sorry, you lost {bet}. Your new balance is {user_data["balance"]} 🪙'
                    ),
                    colour=discord.Colour.red(),
                )
            )

    @app_commands.command(
        name="snakeeyes",
        description="Gamble your 🪙 in a snake eyes game for a chance to win big!",
    )
    @app_commands.checks.cooldown(1, 25, key=lambda i: (i.user.id))
    @app_commands.describe(bet="The amount of 🪙 you want to bet")
    async def snakeeyes(self, interaction: discord.Interaction, bet: int):
        user_data = await DataManager.get_user_data(interaction.user.id)

        if bet > user_data["balance"]:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You do not have enough 🪙 for that bet",
                    colour=discord.Colour.orange(),
                )
            )

        roll1 = random.randint(1, 6)
        roll2 = random.randint(1, 6)

        if roll1 == 1 and roll2 == 1:
            await DataManager.edit_user_data(
                interaction.user.id, "balance", user_data["balance"] + 30 * bet
            )

            await interaction.response.send_message(
                embed=discord.Embed(
                    title="SNAKE EYES!",
                    description=(f"You rolled Snake Eyes! You won {30 * bet} 🪙!"),
                    colour=discord.Colour.green(),
                )
            )

        elif roll1 == 1 or roll2 == 1:
            await DataManager.edit_user_data(
                interaction.user.id, "balance", int(user_data["balance"] + 1.5 * bet)
            )

            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Snake Eye!",
                    description=(
                        f"You rolled 1 snake eye! You won {int(1.5 * bet)} 🪙!"
                    ),
                    colour=discord.Colour.green(),
                )
            )
        else:
            await DataManager.edit_user_data(
                interaction.user.id, "balance", user_data["balance"] - bet
            )

            await interaction.response.send_message(
                embed=discord.Embed(
                    title="You lost",
                    description=(
                        f"You rolled a {roll1} and a {roll2}. You lost {bet} 🪙."
                    ),
                    colour=discord.Colour.orange(),
                )
            )

    @app_commands.command(
        name="slots",
        description="Gamble your 🪙 in a slots game for a chance to win big!",
    )
    @app_commands.checks.cooldown(1, 25, key=lambda i: (i.user.id))
    @app_commands.describe(bet="The amount of 🪙 you want to bet")
    async def slots(self, interaction: discord.Interaction, bet: int):
        user_data = await DataManager.get_user_data(interaction.user.id)

        if bet > user_data["balance"]:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You do not have enough 🪙 for that bet",
                    colour=discord.Colour.orange(),
                )
            )

        emojis = ["🍇", "🍊", "🍐", "🍒", "🍋", "🍉", "🍓", "🍌", "🍍"]
        slot1 = random.choice(emojis)
        slot2 = random.choice(emojis)
        slot3 = random.choice(emojis)

        if slot1 == slot2 == slot3:
            await DataManager.edit_user_data(
                interaction.user.id, "balance", user_data["balance"] + 30 * bet
            )

            await interaction.response.send_message(
                embed=discord.Embed(
                    title="JACKPOT!",
                    description=(
                        f"You rolled {slot1}{slot2}{slot3}! You won {30 * bet} 🪙!"
                    ),
                    colour=discord.Colour.green(),
                )
            )

        elif slot1 == slot2:
            await DataManager.edit_user_data(
                interaction.user.id, "balance", int(user_data["balance"] + 1.5 * bet)
            )

            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Two in a row!",
                    description=(
                        f"You rolled {slot1}{slot2}{slot3}! You won {int(1.5 * bet)} 🪙!"
                    ),
                    colour=discord.Colour.green(),
                )
            )

        else:
            await DataManager.edit_user_data(
                interaction.user.id, "balance", user_data["balance"] - bet
            )

            await interaction.response.send_message(
                embed=discord.Embed(
                    title="You lost",
                    description=(
                        f"You rolled {slot1}{slot2}{slot3}. You lost {bet} 🪙."
                    ),
                    colour=discord.Colour.orange(),
                )
            )


async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(Gambling(bot))
