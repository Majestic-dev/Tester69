import asyncio
import random
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

from utils import DataManager


class Choices(discord.ui.View):
    def __init__(self, executer, bet, disabled_ddown=None, disabled_forfeit=None):
        super().__init__()
        self.choice = None
        self.executer = executer

        self.ddown.disabled = disabled_ddown
        self.forfeit.disabled = disabled_forfeit

        self.ddown.label = f"Double Down ({bet})"
        self.forfeit.label = f"Forfeit (Return {bet // 2})"

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.blurple)
    async def hit(self, interaction: discord.Interaction, _: discord.ui.Button):
        if interaction.user.id != self.executer:
            return await interaction.response.send_message(
                "This isn't yours!", ephemeral=True
            )

        self.choice = "hit"
        await interaction.response.defer()

        self.stop()

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.primary)
    async def stand(self, interaction: discord.Interaction, _: discord.ui.Button):
        if interaction.user.id != self.executer:
            return await interaction.response.send_message(
                "This isn't yours!", ephemeral=True
            )

        self.choice = "stand"
        await interaction.response.defer()

        self.stop()

    @discord.ui.button(label="Double Down", style=discord.ButtonStyle.green)
    async def ddown(self, interaction: discord.Interaction, _: discord.ui.Button):
        if interaction.user.id != self.executer:
            return await interaction.response.send_message(
                "This isn't yours!", ephemeral=True
            )

        self.choice = "ddown"
        await interaction.response.defer()

        self.stop()

    @discord.ui.button(label="Forfeit", style=discord.ButtonStyle.danger)
    async def forfeit(self, interaction: discord.Interaction, _: discord.ui.Button):
        if interaction.user.id != self.executer:
            return await interaction.response.send_message(
                "This isn't yours!", ephemeral=True
            )

        self.choice = "forfeit"
        await interaction.response.defer()

        self.stop()


def sum_of_hand(hand: list):
    _sum = sum(
        [card[1] for card in hand if card[1] not in ["J", "Q", "K", "A"]]
        + [10 for card in hand if card[1] in ["J", "Q", "K"]]
    )

    for _ in [card for card in hand if card[1] == "A"]:
        if _sum + 11 <= 21:
            _sum += 11
        else:
            _sum += 1

    return _sum


def prettify_cards(hand: list):
    res = ""
    for group in [hand[i : i + 3] for i in range(0, len(hand), 3)]:
        for card in group:
            res += (
                f"[``{card[0]}{card[1]}``](https://github.com/MajesticCodes/Tester69)"
            )
        res += "\n"
    return res[:-1]


class Gambling(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="gamble", description="Gamble your set amount of coins")
    async def _gamble(self, interaction: discord.Interaction, bet: int):
        user_data = DataManager.get_user_data(interaction.user.id)

        if bet < 10 or bet > 250000:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Bet Failed",
                    description="You have to add a bet between 10 and 250000",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.orange(),
                )
            )
            return

        if bet > user_data["balance"]:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="No Coins To Gamble",
                    description=(
                        f'You do not have enough funds to gamble. Your balance is {user_data["balance"]}'
                    ),
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.orange(),
                )
            )

        DataManager.edit_user_data(
            interaction.user.id, "balance", user_data["balance"] - bet
        )

        win = random.choices([True, False], [45, 55])[0]
        random1 = random.randint(1, 3)
        winnings = (bet * random1)
        if win:
            DataManager.edit_user_data(
                interaction.user.id, "balance", user_data["balance"] + winnings
            )

            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Bet Results",
                    description=(
                        f'Congratulations! You won {winnings} and your new balance is {user_data["balance"]}'
                    ),
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.green(),
                )
            )

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Bet Results",
                description=(
                    f'Sorry, you lost {bet}. Your new balance is {user_data["balance"]}'
                ),
                timestamp=datetime.utcnow(),
                colour=discord.Colour.red(),
            )
        )

    @app_commands.command(
        name="snakeeyes",
        description="Gamble your coins in a snake eyes game for a chance to win big!",
    )
    async def snakeeyes(self, interaction: discord.Interaction, bet: int):
        user_data = DataManager.get_user_data(interaction.user.id)

        if bet < 10 or bet > 250000:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Bet Failed",
                    description="You have to add a bet between 10 and 250000",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.orange(),
                )
            )
            return

        if bet > user_data["balance"]:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Not Enough Coins",
                    description="You do not have enough coins for that bet",
                    timestamp=datetime.utcnow(),
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
                    timestamp=datetime.utcnow(),
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
                    timestamp=datetime.utcnow(),
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
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.orange(),
                )
            )

    @app_commands.command(
        name="blackjack",
        description="Gamble your coins in a game of blackjack",
    )
    async def blackjack(self, interaction: discord.Interaction, bet: int):
        user_data = DataManager.get_user_data(interaction.user.id)

        if bet < 10 or bet > 250000:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Bet Failed",
                    description="You have to add a bet between 10 and 250000.",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.orange(),
                )
            )

        if bet > user_data["balance"]:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Bet Failed",
                    description="You do not have enough coins for that bet",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.orange(),
                )
            )

        await interaction.response.send_message(
            content="loading blackjack game...",
        )

        deck = [
            (suit, value) for suit in ["♠", "♥", "♦", "♣"] for value in range(2, 11)
        ] + [
            (suit, value)
            for suit in ["♠", "♥", "♦", "♣"]
            for value in ["J", "Q", "K", "A"]
        ]

        random.shuffle(deck)

        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [dealer_first_card := deck.pop(), deck.pop()]

        while sum_of_hand(dealer_hand) <= 16:
            dealer_hand.append(deck.pop())

        if sum_of_hand(player_hand) == 21:
            e = discord.Embed(
                title="Blackjack",
                description=f"You got blackjack! You won {int(bet * 2.5)} coins.",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.green(),
            )

            e.add_field(
                name="Your Hand",
                value=f"{prettify_cards(player_hand)}\nSum: {sum_of_hand(player_hand)}",
            )

            e.add_field(
                name="Dealer Hand",
                value=f"{prettify_cards(dealer_hand)}\nSum: {sum_of_hand(dealer_hand)}",
            )

            await interaction.edit_original_response(
                content=None,
                embed=e,
                view=None,
            )

            DataManager.edit_user_data(
                interaction.user.id, "balance", user_data["balance"] + int(bet * 1.5)
            )

            return

        e = discord.Embed(
            title="Blackjack",
            description=f"Use the buttons below to play.\nBet: {bet}",
            timestamp=datetime.utcnow(),
            colour=discord.Colour.blurple(),
        )

        e.add_field(
            name="Your Hand",
            value=f"{prettify_cards(player_hand)}\nSum: {sum_of_hand(player_hand)}",
        )

        e.add_field(
            name="Dealer Hand",
            value=f"[``{dealer_first_card[0]}{dealer_first_card[1]}``](https://github.com/Majestic-dev/Tester69) ??\nSum: ?",
        )

        view = Choices(interaction.user.id, bet)

        if user_data["balance"] - bet * 2 < 0:
            view.ddown.disabled = True

        await interaction.edit_original_response(content=None, embed=e, view=view)

        while True:
            await view.wait()

            if view.choice == "stand":
                player_hand_value, dealer_hand_value = sum_of_hand(
                    player_hand
                ), sum_of_hand(dealer_hand)

                if player_hand_value > 21:
                    e = discord.Embed(
                        title="Blackjack",
                        description=f"You busted! You lost {bet} coins.",
                        timestamp=datetime.utcnow(),
                        colour=discord.Colour.red(),
                    )

                    e.add_field(
                        name="Your Hand",
                        value=f"{prettify_cards(player_hand)}\nSum: {sum_of_hand(player_hand)}",
                    )

                    e.add_field(
                        name="Dealer Hand",
                        value=f"{prettify_cards(dealer_hand)}\nSum: {sum_of_hand(dealer_hand)}",
                    )

                    await interaction.edit_original_response(
                        content=None, embed=e, view=None
                    )

                    DataManager.edit_user_data(
                        interaction.user.id, "balance", user_data["balance"] - bet
                    )

                    return

                if dealer_hand_value > 21:
                    e = discord.Embed(
                        title="Blackjack",
                        description=f"The dealer busted! You won {bet} coins.",
                        timestamp=datetime.utcnow(),
                        colour=discord.Colour.green(),
                    )

                    e.add_field(
                        name="Your Hand",
                        value=f"{prettify_cards(player_hand)}\nSum: {sum_of_hand(player_hand)}",
                    )

                    e.add_field(
                        name="Dealer Hand",
                        value=f"{prettify_cards(dealer_hand)}\nSum: {sum_of_hand(dealer_hand)}",
                    )

                    await interaction.edit_original_response(
                        content=None, embed=e, view=None
                    )

                    DataManager.edit_user_data(
                        interaction.user.id, "balance", user_data["balance"] + bet
                    )

                    return

                if player_hand_value > dealer_hand_value:
                    e = discord.Embed(
                        title="Blackjack",
                        description=f"You won! You won {bet} coins.",
                        timestamp=datetime.utcnow(),
                        colour=discord.Colour.green(),
                    )

                    e.add_field(
                        name="Your Hand",
                        value=f"{prettify_cards(player_hand)}\nSum: {sum_of_hand(player_hand)}",
                    )

                    e.add_field(
                        name="Dealer Hand",
                        value=f"{prettify_cards(dealer_hand)}\nSum: {sum_of_hand(dealer_hand)}",
                    )

                    await interaction.edit_original_response(
                        content=None, embed=e, view=None
                    )

                    DataManager.edit_user_data(
                        interaction.user.id, "balance", user_data["balance"] + bet
                    )

                    return

                if player_hand_value == dealer_hand_value:
                    e = discord.Embed(
                        title="Blackjack",
                        description=f"You tied! You got your bet back.",
                        timestamp=datetime.utcnow(),
                        colour=discord.Colour.orange(),
                    )

                    e.add_field(
                        name="Your Hand",
                        value=f"{prettify_cards(player_hand)}\nSum: {sum_of_hand(player_hand)}",
                    )

                    e.add_field(
                        name="Dealer Hand",
                        value=f"{prettify_cards(dealer_hand)}\nSum: {sum_of_hand(dealer_hand)}",
                    )

                    await interaction.edit_original_response(
                        content=None, embed=e, view=None
                    )

                    return

                if player_hand_value < dealer_hand_value:
                    e = discord.Embed(
                        title="Blackjack",
                        description=f"You lost! You lost {bet} coins.",
                        timestamp=datetime.utcnow(),
                        colour=discord.Colour.red(),
                    )

                    e.add_field(
                        name="Your Hand",
                        value=f"{prettify_cards(player_hand)}\nSum: {sum_of_hand(player_hand)}",
                    )

                    e.add_field(
                        name="Dealer Hand",
                        value=f"{prettify_cards(dealer_hand)}\nSum: {sum_of_hand(dealer_hand)}",
                    )

                    await interaction.edit_original_response(
                        content=None, embed=e, view=None
                    )

                    DataManager.edit_user_data(
                        interaction.user.id, "balance", user_data["balance"] - bet
                    )

                    return

            elif view.choice == "forfeit":
                e = discord.Embed(
                    title="Blackjack",
                    description=f"You forfeited! You lost {bet / 2} coins. 50% of your bet was returned.",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.red(),
                )

                e.add_field(
                    name="Your Hand",
                    value=f"{prettify_cards(player_hand)}\nSum: {sum_of_hand(player_hand)}",
                )

                e.add_field(
                    name="Dealer Hand",
                    value=f"{prettify_cards(dealer_hand)}\nSum: {sum_of_hand(dealer_hand)}",
                )

                await interaction.edit_original_response(
                    content=None, embed=e, view=None
                )

                DataManager.edit_user_data(
                    interaction.user.id, "balance", int(user_data["balance"] - bet / 2)
                )

                return

            elif view.choice == "ddown":
                player_hand.append(deck.pop())

                bet *= 2
                if player_hand_value == 21:
                    break

                player_hand_value, dealer_hand_value = sum_of_hand(
                    player_hand
                ), sum_of_hand(dealer_hand)

                if player_hand_value > 21:
                    e = discord.Embed(
                        title="Blackjack",
                        description=f"You busted! You lost {bet} coins.",
                        timestamp=datetime.utcnow(),
                        colour=discord.Colour.red(),
                    )

                    e.add_field(
                        name="Your Hand",
                        value=f"{prettify_cards(player_hand)}\nSum: {sum_of_hand(player_hand)}",
                    )

                    e.add_field(
                        name="Dealer Hand",
                        value=f"{prettify_cards(dealer_hand)}\nSum: {sum_of_hand(dealer_hand)}",
                    )

                    await interaction.edit_original_response(
                        content=None, embed=e, view=None
                    )

                    DataManager.edit_user_data(
                        interaction.user.id, "balance", user_data["balance"] - bet
                    )

                    return

                if dealer_hand_value > 21:
                    e = discord.Embed(
                        title="Blackjack",
                        description=f"The dealer busted! You won {bet} coins.",
                        timestamp=datetime.utcnow(),
                        colour=discord.Colour.green(),
                    )

                    e.add_field(
                        name="Your Hand",
                        value=f"{prettify_cards(player_hand)}\nSum: {sum_of_hand(player_hand)}",
                    )

                    e.add_field(
                        name="Dealer Hand",
                        value=f"{prettify_cards(dealer_hand)}\nSum: {sum_of_hand(dealer_hand)}",
                    )

                    await interaction.edit_original_response(
                        content=None, embed=e, view=None
                    )

                    DataManager.edit_user_data(
                        interaction.user.id, "balance", user_data["balance"] + bet
                    )

                    return

                if player_hand_value > dealer_hand_value:
                    e = discord.Embed(
                        title="Blackjack",
                        description=f"You won! You won {bet} coins.",
                        timestamp=datetime.utcnow(),
                        colour=discord.Colour.green(),
                    )

                    e.add_field(
                        name="Your Hand",
                        value=f"{prettify_cards(player_hand)}\nSum: {sum_of_hand(player_hand)}",
                    )

                    e.add_field(
                        name="Dealer Hand",
                        value=f"{prettify_cards(dealer_hand)}\nSum: {sum_of_hand(dealer_hand)}",
                    )

                    await interaction.edit_original_response(
                        content=None, embed=e, view=None
                    )

                    DataManager.edit_user_data(
                        interaction.user.id, "balance", user_data["balance"] + bet
                    )

                    return

                if player_hand_value == dealer_hand_value:
                    e = discord.Embed(
                        title="Blackjack",
                        description=f"You tied! You got your bet back.",
                        timestamp=datetime.utcnow(),
                        colour=discord.Colour.orange(),
                    )

                    e.add_field(
                        name="Your Hand",
                        value=f"{prettify_cards(player_hand)}\nSum: {sum_of_hand(player_hand)}",
                    )

                    e.add_field(
                        name="Dealer Hand",
                        value=f"{prettify_cards(dealer_hand)}\nSum: {sum_of_hand(dealer_hand)}",
                    )

                    await interaction.edit_original_response(
                        content=None, embed=e, view=None
                    )

                    return

                if player_hand_value < dealer_hand_value:
                    e = discord.Embed(
                        title="Blackjack",
                        description=f"You lost! You lost {bet} coins.",
                        timestamp=datetime.utcnow(),
                        colour=discord.Colour.red(),
                    )

                    e.add_field(
                        name="Your Hand",
                        value=f"{prettify_cards(player_hand)}\nSum: {sum_of_hand(player_hand)}",
                    )

                    e.add_field(
                        name="Dealer Hand",
                        value=f"{prettify_cards(dealer_hand)}\nSum: {sum_of_hand(dealer_hand)}",
                    )

                    await interaction.edit_original_response(
                        content=None, embed=e, view=None
                    )

                    DataManager.edit_user_data(
                        interaction.user.id, "balance", user_data["balance"] - bet
                    )

                    return

            elif view.choice == "hit":
                player_hand.append(random.choice(deck))
                player_hand_value = sum_of_hand(player_hand)

                if player_hand_value == 21:
                    break

                if player_hand_value > 21:
                    e = discord.Embed(
                        title="Blackjack",
                        description=f"You busted! You lost {bet} coins.",
                        timestamp=datetime.utcnow(),
                        colour=discord.Colour.red(),
                    )

                    e.add_field(
                        name="Your Hand",
                        value=f"{prettify_cards(player_hand)}\nSum: {sum_of_hand(player_hand)}",
                    )

                    e.add_field(
                        name="Dealer Hand",
                        value=f"{prettify_cards(dealer_hand)}\nSum: {sum_of_hand(dealer_hand)}",
                    )

                    await interaction.edit_original_response(
                        content=None, embed=e, view=None
                    )

                    DataManager.edit_user_data(
                        interaction.user.id, "balance", user_data["balance"] - bet
                    )

                    return

                e = discord.Embed(
                    title="Blackjack",
                    description=f"Bet: {bet} coins",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.blue(),
                )

                e.add_field(
                    name="Your Hand",
                    value=f"{prettify_cards(player_hand)}\nSum: {sum_of_hand(player_hand)}",
                )

                e.add_field(
                    name="Dealer Hand",
                    value=f"[``{dealer_first_card[0]}{dealer_first_card[1]}``](https://github.com/MajesticCodes/Tester69) ??\nSum: ?",
                )

                view = Choices(interaction.user.id, bet, True, True)

                await interaction.edit_original_response(
                    content=None, embed=e, view=view
                )

    @app_commands.command(
        name="coinflip", description="Bet your coins in a game of coinflip"
    )
    @app_commands.choices(
        choices=[
            app_commands.Choice(name="Heads", value="heads"),
            app_commands.Choice(name="Tails", value="tails"),
        ]
    )
    async def coinflip(
        self,
        interaction: discord.Interaction,
        bet: int,
        choices: app_commands.Choice[str],
    ):
        user_data = DataManager.get_user_data(interaction.user.id)

        if bet < 10 or bet > 250000:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Bet Failed",
                    description="You have to add a bet between 10 and 250000",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.orange(),
                )
            )

        if bet > user_data["balance"]:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Bet Failed",
                    description="You do not have enough coins for that bet",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.orange(),
                )
            )

        DataManager.edit_user_data(
            interaction.user.id, "balance", user_data["balance"] - bet
        )

        result = random.choices(("heads", "tails"))[0]

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Flipping A Coin!",
                description="Flipping a coin <a:coinflip:1088886954713694398>",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.green(),
            )
        )
        await asyncio.sleep(3)

        if choices.value != result:
            return await interaction.edit_original_response(
                embed=discord.Embed(
                    title="You Lose!",
                    description=f"The coin landed on {result}, you lose {bet} coins!",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.red(),
                )
            )

        DataManager.edit_user_data(
            interaction.user.id, "balance", user_data["balance"] + bet * 2
        )

        await interaction.edit_original_response(
            embed=discord.Embed(
                title="You Won!",
                description=f"The coin landed on {result}, you win {bet} coins!",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.green(),
            )
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Gambling(bot))
