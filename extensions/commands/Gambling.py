from discord.ext import commands
from discord import app_commands
import discord
import json
import random

Start = discord.Embed(
    title="ERROR",
    description="You need to execute the `/start` command before executing any other commands",
    colour=discord.Colour.dark_orange(),
)


def load_data():
    try:
        with open("data/users.json", "r") as f:
            return json.load(f)
    except:
        print("Could not load data")


def save_data(data):
    with open("data/users.json", "w") as f:
        json.dump(data, f, indent=4)


class Gambling(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="gamble", description="Gamble your set amount of coins")
    async def _gamble(self, interaction: discord.Interaction, bet: int = None):
        user_id = str(interaction.user.id)
        data = load_data()

        if user_id not in data:
            await interaction.response.send_message(embed=Start)
            return

        NotGoodBet = discord.Embed(
            title="Bet Failed",
            description="You have to add a bet between 0 and 10000000, for example `'gamble 10`",
            colour=discord.Colour.orange(),
        )

        if bet is None or bet < 0 or bet > 10000000:
            await interaction.response.send_message(embed=NotGoodBet)
            return

        TooHighBet = discord.Embed(
            title="Too High Bet",
            description=(f"You cannot bet more than 10 million coins"),
            colour=discord.Colour.orange(),
        )

        NoFunds = discord.Embed(
            title="No Coins To Gamble",
            description=(
                f'You do not have enough funds to gamble. Your balance is {data[user_id]["balance"]}'
            ),
            colour=discord.Colour.orange(),
        )

        NoFunds2 = discord.Embed(
            title="No Coins To Gamble",
            description=(
                f'You do not have enough funds to gamble. Your balance is {data[user_id]["balance"]}'
            ),
            colour=discord.Colour.orange(),
        )

        if user_id in data:
            if bet > 10000000:
                await interaction.response.send_message(embed=TooHighBet)
                return
            if bet > data[user_id]["balance"]:
                await interaction.response.send_message(embed=NoFunds)
                return
            data[user_id]["balance"] -= bet
            save_data(data)
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
                data[user_id]["balance"] += winnings
                save_data(data)

                BetWinnings = discord.Embed(
                    title="Bet Results",
                    description=(
                        f'Congratulations! You won {winnings - bet} and your new balance is {data[user_id]["balance"]}'
                    ),
                    colour=discord.Colour.green(),
                )

                print(
                    f"{interaction.user.id} won at a {multiplier}x multiplier with a {chances[multipliers.index(multiplier)]}% chance and total winnings of {winnings}"
                )

                await interaction.response.send_message(embed=BetWinnings)
            else:

                BetLoss = discord.Embed(
                    title="Bet Results",
                    description=(
                        f'Sorry, you lost {bet}. Your new balance is {data[user_id]["balance"]}'
                    ),
                    colour=discord.Colour.red(),
                )

                await interaction.response.send_message(embed=BetLoss)
        else:
            await interaction.response.send_message(embed=NoFunds2)

    @app_commands.command(
        name="snakeeyes",
        description="Gamble your coins in a snake eyes game for a chance to win big!",
    )
    async def snakeeyes(self, interaction: discord.Interaction, bet: int):
        Nocoins = discord.Embed(
            title="Not Enough Coins",
            description="You do not have enough coins for that bet",
            colour=discord.Colour.orange(),
        )

        user_id = str(interaction.user.id)

        data = load_data()

        if user_id not in data:
            await interaction.response.send_message(embed=Start)
            return

        if bet > data[user_id]["balance"]:
            await interaction.response.send_message(embed=Nocoins)
            return

        roll1 = random.randint(1, 6)
        roll2 = random.randint(1, 6)
        if roll1 == 1 and roll2 == 1:
            data[user_id]["balance"] += 30 * bet
            save_data(data)

            Snakeeyes = discord.Embed(
                title="SNAKE EYES!",
                description=(f"You rolled Snake Eyes! You won {30 * bet} coins!"),
                colour=discord.Colour.green(),
            )

            await interaction.response.send_message(embed=Snakeeyes)

        elif roll1 == 1 or roll2 == 1:
            data[user_id]["balance"] += 1.5 * bet
            save_data(data)

            Snakeeye = discord.Embed(
                title="Snake Eye!",
                description=(f"You rolled 1 snake eye! You won {1.5 * bet} coins!"),
                colour=discord.Colour.green(),
            )

            await interaction.response.send_message(embed=Snakeeye)
        else:
            data[user_id]["balance"] -= bet
            save_data(data)

            Betloss = discord.Embed(
                title="You lost",
                description=(
                    f"You rolled a {roll1} and a {roll2}. You lost {bet} coins."
                ),
                colour=discord.Colour.orange(),
            )

            await interaction.response.send_message(embed=Betloss)


async def setup(bot: commands.Bot):
    await bot.add_cog(Gambling(bot))