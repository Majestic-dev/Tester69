import json
import random
import string
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from utils import DataManager, Paginator, cooldown_check


class leaderboard_dropdown(discord.ui.Select):
    def __init__(self, bot: commands.AutoShardedBot, interaction: discord.Interaction):
        self.bot = bot
        self.executer = interaction.user.id

        options = [
            discord.SelectOption(
                label="Cash",
                value="cash",
                description="Cash Balance Leaderboard",
                emoji="💸",
            ),
            discord.SelectOption(
                label="Bank",
                value="bank",
                description="Bank Balance Leaderboard",
                emoji="🏦",
            ),
        ]
        super().__init__(
            placeholder="Choose a leaderboard type",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.executer:
            return await interaction.response.send_message(
                ephemeral=True,
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> This isn't yours",
                    colour=discord.Colour.red(),
                ),
            )

        if self.values[0] == "cash":
            user_ids = await DataManager.get_all_users()
            users = {
                user_id: await DataManager.get_user_data(user_id)
                for user_id in user_ids
            }
            top_10 = sorted(users, key=lambda k: users[k]["balance"], reverse=True)[:10]

            lb_embed = discord.Embed(
                colour=discord.Colour.green(),
            )

            for i, user in enumerate(top_10):
                lb_embed.add_field(
                    name=f"{i + 1}. {self.bot.get_user(int(user))}",
                    value=f"**Wallet:** `{users[user]['balance']}` 🪙",
                    inline=False,
                )

            lb_embed.set_author(name="Cash Leaderboard", icon_url=self.bot.user.avatar)
            await interaction.response.edit_message(
                content=None,
                embed=lb_embed,
                view=leaderboard_dropdown_view(bot=self.bot, interaction=interaction),
            )

        elif self.values[0] == "bank":
            user_ids = await DataManager.get_all_users()
            users = {
                user_id: await DataManager.get_user_data(user_id)
                for user_id in user_ids
            }
            top_10 = sorted(users, key=lambda k: users[k]["bank"], reverse=True)[:10]

            lb_embed = discord.Embed(
                colour=discord.Colour.green(),
            )

            for i, user in enumerate(top_10):
                lb_embed.add_field(
                    name=f"{i + 1}. {self.bot.get_user(int(user))}",
                    value=f"**Bank:** `{users[user]['bank']}` 🪙",
                    inline=False,
                )

            lb_embed.set_author(name="Bank Leaderboard", icon_url=self.bot.user.avatar)
            await interaction.response.edit_message(
                embed=lb_embed,
                view=leaderboard_dropdown_view(bot=self.bot, interaction=interaction),
            )


class leaderboard_dropdown_view(discord.ui.View):
    def __init__(self, bot: commands.AutoShardedBot, interaction: discord.Interaction):
        self.bot = bot
        super().__init__()

        self.add_item(leaderboard_dropdown(bot=self.bot, interaction=interaction))


def random_choice_from_dict(d):
    total_chance = sum(item["chance"] for item in d.values())
    rand = random.uniform(0, total_chance)
    for item_name, item_data in d.items():
        if rand < item_data["chance"]:
            return item_name, item_data
        rand -= item_data["chance"]


class economy(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @app_commands.command(name="pay", description="Pay someone some 🪙")
    @app_commands.checks.cooldown(1, 600, key=lambda i: (i.user.id))
    @app_commands.describe(
        user="The user you want to send the money to",
        amount="The amount of money you want to send",
    )
    async def pay(
        self, interaction: discord.Interaction, user: discord.User, amount: int
    ):
        if user.id == interaction.user.id:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You can't pay yourself!",
                    colour=discord.Colour.red(),
                )
            )

        if amount <= 0:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You can't pay someone a negative amount!",
                    colour=discord.Colour.red(),
                )
            )

        payer_data = await DataManager.get_user_data(interaction.user.id)
        if payer_data["balance"] < amount:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You don't have enough 🪙 to pay that amount!",
                    colour=discord.Colour.red(),
                )
            )

        await DataManager.edit_user_data(
            interaction.user.id, "balance", payer_data["balance"] - amount
        )

        receiver_data = await DataManager.get_user_data(user.id)
        await DataManager.edit_user_data(
            user.id, "balance", receiver_data["balance"] + amount
        )

        payer_data = await DataManager.get_user_data(interaction.user.id)

        await interaction.response.send_message(
            embed=discord.Embed(
                description=f'<:white_checkmark:1096793014287995061> Paid {user.mention} {amount} 🪙. Your new balance is {payer_data["balance"]} 🪙',
                colour=discord.Colour.green(),
            )
        )

    @app_commands.command(name="balance", description="Check your 🪙 balance")
    @app_commands.checks.cooldown(1, 20, key=lambda i: (i.user.id))
    @app_commands.describe(
        user="The user you want to check the balance of (yours if no user is provided)"
    )
    async def balance(
        self, interaction: discord.Interaction, user: Optional[discord.User] = None
    ):
        await interaction.response.defer()
        if user == None:
            user_data = await DataManager.get_user_data(interaction.user.id)
            await interaction.edit_original_response(
                embed=discord.Embed(
                    title=f"{interaction.user}'s Balance",
                    description=(
                        f'**💸 Wallet:** {user_data["balance"]} 🪙\n**🏦 Bank:** {user_data["bank"]} 🪙'
                    ),
                    colour=discord.Colour.green(),
                )
            )
        else:
            user_data = await DataManager.get_user_data(user.id)
            await interaction.edit_original_response(
                embed=discord.Embed(
                    title=f"{user}'s Balance",
                    description=(
                        f'**💸 Wallet:** {user_data["balance"]} 🪙\n**🏦 Bank:** {user_data["bank"]} 🪙'
                    ),
                    colour=discord.Colour.green(),
                )
            )

    @app_commands.command(
        name="hunt",
        description="Grab a rifle from the shop and go hunting for some animals",
    )
    async def hunt(self, interaction: discord.Interaction):
        if await cooldown_check(interaction.user.id, "hunt", 600):
            chances = []
            for item in DataManager.get("economy", "hunting items").values():
                chances.append(item["chance"])
            items = list(DataManager.get("economy", "hunting items").keys())
            item_name = random.choices(items, weights=chances, k=1)
            item_emoji = DataManager.get("economy", "items")[item_name[0]]["emoji"]
            user_data = await DataManager.get_user_data(interaction.user.id)

            if user_data["inventory"] is not None:
                inventory = json.loads(user_data["inventory"])
            else:
                inventory = {}

            if (
                user_data["inventory"] is None
                or "hunting rifle" not in user_data["inventory"]
                or inventory["hunting rifle"] == 0
            ):
                item_emoji = DataManager.get("economy", "items")["hunting rifle"]["emoji"]
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        description=f"<:white_cross:1096791282023669860> You need a **{item_emoji} Hunting Rifle** to hunt some animals `/buy_item`",
                        colour=discord.Colour.red(),
                    )
                )

            await DataManager.edit_user_inventory(interaction.user.id, item_name[0], 1)

            await interaction.response.send_message(
                embed=discord.Embed(
                    description=f"You hunted down a **{item_emoji} {item_name[0]}**",
                    colour=discord.Colour.green(),
                )
            )

    @app_commands.command(
        name="fish",
        description="Grab a fishing pole from the shop and go fishing for some fish",
    )
    async def fish(self, interaction: discord.Interaction):
        if await cooldown_check(interaction.user.id, "fish", 600):
            chances = []
            for item in DataManager.get("economy", "fishing items").values():
                chances.append(item["chance"])
            items = list(DataManager.get("economy", "fishing items").keys())
            item_name = random.choices(items, weights=chances, k=1)
            item_emoji = DataManager.get("economy", "items")[item_name[0]]["emoji"]
            user_data = await DataManager.get_user_data(interaction.user.id)

            if user_data["inventory"] is not None:
                inventory = json.loads(user_data["inventory"])
            else:
                inventory = {}

            if (
                user_data["inventory"] is None
                or "fishing pole" not in user_data["inventory"]
                or inventory["fishing pole"] == 0
            ):
                item_emoji = DataManager.get("economy", "items")["fishing pole"]["emoji"]
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        description=f"<:white_cross:1096791282023669860> You need a **{item_emoji} Fishing Pole** to fish `/buy_item`",
                        colour=discord.Colour.red(),
                    )
                )

            await DataManager.edit_user_inventory(interaction.user.id, item_name[0], 1)

            await interaction.response.send_message(
                embed=discord.Embed(
                    description=f"You caught a **{item_emoji} {item_name[0]}**",
                    colour=discord.Colour.green(),
                )
            )

    async def item_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        user_data = await DataManager.get_user_data(interaction.user.id)
        items_in_inventory = json.loads(user_data["inventory"]).keys()

        return [
            app_commands.Choice(name=item, value=item)
            for item in items_in_inventory
            if item.lower().startswith(current.lower())
            or len(current) < 1
            and user_data["inventory"][item] > 0
        ]

    @app_commands.command(name="sell", description="Sell your loot for 🪙")
    @app_commands.autocomplete(item=item_autocomplete)
    @app_commands.checks.cooldown(1, 15, key=lambda i: (i.user.id))
    @app_commands.describe(
        item="The item you want to sell",
        amount="The amount of the item you want to sell (defaults to 1)",
    )
    async def sell(self, interaction: discord.Interaction, item: str, amount: int = 1):
        if amount <= 0:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You can't sell 0 or a negative amount of items",
                    colour=discord.Colour.red(),
                )
            )

        items = DataManager.get("economy", "items")
        if not items:
            print("where are the items gang")

        user_data = await DataManager.get_user_data(interaction.user.id)

        if user_data["inventory"] is not None and json.loads(user_data["inventory"]):
            user_inv = json.loads(user_data["inventory"])
        else:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You don't have any items in your inventory",
                    colour=discord.Colour.orange(),
                )
            )

        item1 = items.get(item.lower(), None)

        if item1:
            if (
                user_data["inventory"] is None
                or item.lower() not in user_data["inventory"]
            ):
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        description="<:white_cross:1096791282023669860> You don't have any of that item",
                        colour=discord.Colour.orange(),
                    )
                )

            if int(user_inv[item]) < amount:
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        description="<:white_cross:1096791282023669860> You don't have enough of that item",
                        colour=discord.Colour.orange(),
                    )
                )

            price = item1["sell price"]
            await DataManager.edit_user_data(
                interaction.user.id,
                "balance",
                user_data["balance"] + (int(amount) * price),
            )
            await DataManager.edit_user_inventory(
                interaction.user.id, item, -int(amount)
            )

            await interaction.response.send_message(
                embed=discord.Embed(
                    description=f"<:white_checkmark:1096793014287995061> Sold {amount} **{item1['emoji']} {item1['name']}** for **{(int(amount) * price)} 🪙**",
                    colour=discord.Colour.green(),
                )
            )
        else:
            await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> That item doesn't exist",
                    colour=discord.Colour.red(),
                )
            )

    @app_commands.command(
        name="rob", description="Rob the mentioned user out of their 🪙"
    )
    @app_commands.checks.cooldown(1, 3600, key=lambda i: (i.user.id))
    @app_commands.describe(user="The user you want to rob")
    async def rob(self, interaction: discord.Interaction, user: discord.User):
        robber_data = await DataManager.get_user_data(interaction.user.id)
        robber_balance = robber_data["balance"]
        robber_bank = robber_data["bank"]
        victim_data = await DataManager.get_user_data(user.id)
        victim_balance = victim_data["balance"]

        if interaction.user.id == user.id:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> Can't rob yourself, try mentioning another user",
                    colour=discord.Colour.orange(),
                )
            )

        if victim_balance == 0:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description=f"<:white_cross:1096791282023669860> Can't rob {user.mention} since they do not have any 🪙 to rob!",
                    colour=discord.Colour.orange(),
                )
            )

        successfulrob = random.choices([True, False])[0]
        if successfulrob == True:
            percentage = random.randint(10, 75) / 100
            cash = int(victim_balance * percentage)
            await DataManager.edit_user_data(
                user.id, "balance", victim_data["balance"] - cash
            )
            await DataManager.edit_user_data(
                interaction.user.id, "balance", robber_data["balance"] + cash
            )

            return await interaction.response.send_message(
                embed=discord.Embed(
                    description=f"<:white_checkmark:1096793014287995061> You flee from the cops as you robbed {user.mention} out of {cash} 🪙",
                    colour=discord.Colour.green(),
                )
            )

        elif successfulrob == False:
            percentage = random.randint(20, 50) / 100
            if robber_balance != 0:
                cash = int(robber_balance * percentage)
                await DataManager.edit_user_data(
                    interaction.user.id, "balance", robber_data["balance"] - cash
                )
                await interaction.response.send_message(
                    embed=discord.Embed(
                        description=f"<:white_cross:1096791282023669860> You got caught trying to rob {user.mention} and had to pay the police {cash}",
                        colour=discord.Colour.red(),
                    )
                )
            else:
                cash2 = int(robber_bank * percentage)
                await DataManager.edit_user_data(
                    interaction.user.id, "balance", robber_data["bank"] - cash2
                )
                await interaction.response.send_message(
                    embed=discord.Embed(
                        description=f"<:white_cross:1096791282023669860> You got caught trying to rob <@{user.id}> and had to pay the police {cash2}",
                        colour=discord.Colour.red(),
                    )
                )

    @app_commands.command(
        name="hourly", description="Gain 1000 🪙 every time you use this command"
    )
    async def hourly(self, interaction: discord.Interaction):
        user_data = await DataManager.get_user_data(interaction.user.id)

        if await cooldown_check(interaction.user.id, "hourly", 3600):
            await DataManager.edit_user_data(
                interaction.user.id, "balance", user_data["balance"] + 1000
            )
            await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_checkmark:1096793014287995061> You received 1000 🪙",
                    colour=discord.Colour.green(),
                )
            )

    @app_commands.command(
        name="daily", description="Gain 10000 🪙 every time you use this command"
    )
    async def daily(self, interaction: discord.Interaction):
        user_data = await DataManager.get_user_data(interaction.user.id)

        if await cooldown_check(interaction.user.id, "daily", 86400):
            await DataManager.edit_user_data(
                interaction.user.id, "balance", user_data["balance"] + 10000
            )
            await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_checkmark:1096793014287995061> You received 10000 🪙",
                    colour=discord.Colour.green(),
                )
            )

    @app_commands.command(
        name="weekly", description="Gain 25000 🪙 every time you use the command"
    )
    async def weekly(self, interaction: discord.Interaction):
        user_data = await DataManager.get_user_data(interaction.user.id)

        if await cooldown_check(interaction.user.id, "weekly", 604800):
            await DataManager.edit_user_data(
                interaction.user.id, "balance", user_data["balance"] + 25000
            )
            await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_checkmark:1096793014287995061> You received 25000 🪙",
                    colour=discord.Colour.green(),
                )
            )

    @app_commands.command(
        name="monthly", description="Gain 50000 🪙 every time you use the command"
    )
    async def monthly(self, interaction: discord.Interaction):
        user_data = await DataManager.get_user_data(interaction.user.id)
        
        if await cooldown_check(interaction.user.id, "monthly", 2592000):
            await DataManager.edit_user_data(
                interaction.user.id, "balance", user_data["balance"] + 50000
            )
            await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_checkmark:1096793014287995061> You received 50000 🪙",
                    colour=discord.Colour.green(),
                )
            )

    @app_commands.command(
    name="inventory", description="Check the contents of your inventory"
    )
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    async def inventory(self, interaction: discord.Interaction):
        user_data = await DataManager.get_user_data(interaction.user.id)

        if user_data["inventory"] is None:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You don't have any items in your inventory",
                    colour=discord.Colour.orange(),
                )
            )

        inventory = json.loads(user_data["inventory"])
        items = [(item, count) for item, count in inventory.items() if count != 0]

        if not items:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You don't have any items in your inventory",
                    colour=discord.Colour.orange(),
                )
            )

        embeds = []
        for i in range(0, len(items), 10):
            inv_embed = discord.Embed(colour=discord.Colour.green())
            for item, count in items[i:i+10]:
                name = f"{DataManager.get('economy', 'items')[item.lower()]['emoji']} {item} - {count}"
                inv_embed.add_field(
                    name=f"{name}",
                    value=f"{DataManager.get('economy', 'items')[item.lower()]['type']}",
                    inline=False,
                )
            inv_embed.set_author(
                name=interaction.user.name + "'s inventory" + f" page {i//10 + 1}/" + str(len(items)//10 + 1),
                icon_url=interaction.user.display_avatar,
            )
            embeds.append(inv_embed)

        await Paginator.Simple().paginate(interaction, embeds)

    @app_commands.command(name="deposit", description="Deposit money into your bank")
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    @app_commands.describe(amount="The amount of 🪙 you want to deposit")
    async def deposit(self, interaction: discord.Interaction, amount: str):
        user_data = await DataManager.get_user_data(interaction.user.id)

        if amount == "all":
            if user_data["balance"] != 0:
                await DataManager.edit_user_data(
                    interaction.user.id,
                    "bank",
                    user_data["bank"] + user_data["balance"],
                )
                await DataManager.edit_user_data(
                    interaction.user.id,
                    "balance",
                    user_data["balance"] - user_data["balance"],
                )
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        description="<:white_checkmark:1096793014287995061> Deposited all your 🪙 in the bank",
                        colour=discord.Colour.green(),
                    )
                )
            else:
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        description="<:white_cross:1096791282023669860> You don't have any 🪙 to deposit",
                        colour=discord.Colour.orange(),
                    )
                )

        if amount.isnumeric() == False:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> Enter a valid number as an input",
                    colour=discord.Colour.red(),
                )
            )

        if int(amount) > user_data["balance"]:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You do not have enough money to deposit",
                    colour=discord.Colour.orange(),
                )
            )

        await DataManager.edit_user_data(
            interaction.user.id, "balance", user_data["balance"] - int(amount)
        )
        await DataManager.edit_user_data(
            interaction.user.id, "bank", user_data["bank"] + int(amount)
        )

        await interaction.response.send_message(
            embed=discord.Embed(
                description=f"<:white_checkmark:1096793014287995061> Deposited {amount} 🪙 into your bank",
                colour=discord.Colour.green(),
            )
        )

    @app_commands.command(name="withdraw", description="Withdraw money from your bank")
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    @app_commands.describe(amount="The amount of 🪙 you want to withdraw")
    async def withdraw(self, interaction: discord.Interaction, amount: str):
        user_data = await DataManager.get_user_data(interaction.user.id)

        if amount == "all":
            await DataManager.edit_user_data(
                interaction.user.id, "balance", user_data["balance"] + user_data["bank"]
            )
            await DataManager.edit_user_data(
                interaction.user.id, "bank", user_data["bank"] - user_data["bank"]
            )
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_checkmark:1096793014287995061> Withdrew all your 🪙 from the bank",
                    colour=discord.Colour.green(),
                )
            )

        if amount.isnumeric() == False:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> Enter a valid number as an input",
                    colour=discord.Colour.red(),
                )
            )

        if int(amount) > user_data["bank"]:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You do not have enough money to withdraw",
                    colour=discord.Colour.orange(),
                )
            )

        await DataManager.edit_user_data(
            interaction.user.id, "bank", user_data["bank"] - int(amount)
        )
        await DataManager.edit_user_data(
            interaction.user.id, "balance", user_data["balance"] + int(amount)
        )

        await interaction.response.send_message(
            embed=discord.Embed(
                description=f"<:white_checkmark:1096793014287995061> Withdrew {int(amount)} 🪙 from your bank",
                colour=discord.Colour.green(),
            )
        )

    @app_commands.command(
        name="leaderboard", description="See the top 10 richest people"
    )
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    @app_commands.choices(
        choices=[
            app_commands.Choice(name="💸 Cash", value="cash"),
            app_commands.Choice(name="🏦 Bank", value="bank"),
        ]
    )
    @app_commands.describe(choices="The type of leaderboard you want to see")
    async def leaderboard(
        self, interaction: discord.Interaction, choices: app_commands.Choice[str]
    ):
        view = leaderboard_dropdown_view(bot=self.bot, interaction=interaction)

        if choices.value == "cash":
            user_ids = await DataManager.get_all_users()
            users = {
                user_id: await DataManager.get_user_data(user_id)
                for user_id in user_ids
            }
            top_10 = sorted(users, key=lambda k: users[k]["balance"], reverse=True)[:10]

            lb_embed = discord.Embed(
                colour=discord.Colour.green(),
            )

            for i, user in enumerate(top_10):
                lb_embed.add_field(
                    name=f"{i + 1}. {self.bot.get_user(int(user))}",
                    value=f"**Wallet:** `{users[user]['balance']}` 🪙",
                    inline=False,
                )

            lb_embed.set_author(name="Cash Leaderboard", icon_url=self.bot.user.avatar)
            await interaction.response.send_message(embed=lb_embed, view=view)

        elif choices.value == "bank":
            user_ids = await DataManager.get_all_users()
            users = {
                user_id: await DataManager.get_user_data(user_id)
                for user_id in user_ids
            }
            top_10 = sorted(users, key=lambda k: users[k]["bank"], reverse=True)[:10]

            lb_embed = discord.Embed(
                colour=discord.Colour.green(),
            )

            for i, user in enumerate(top_10):
                lb_embed.add_field(
                    name=f"{i + 1}. {self.bot.get_user(int(user))}",
                    value=f"**Bank:** `{users[user]['bank']}` 🪙",
                    inline=False,
                )

            lb_embed.set_author(name="Bank Leaderboard", icon_url=self.bot.user.avatar)
            await interaction.response.send_message(embed=lb_embed, view=view)

    @app_commands.command(name="shop", description="View the shop to buy various items")
    @app_commands.checks.cooldown(1, 15, key=lambda i: (i.user.id))
    async def shop(self, interaction: discord.Interaction):
        user_data = await DataManager.get_user_data(interaction.user.id)

        embeds = []

        cur_embed = discord.Embed(
            title="Shop", colour=discord.Colour.from_rgb(43, 45, 49)
        )

        for item in DataManager.get("economy", "items"):
            if len(cur_embed.fields) >= 8:
                embeds.append(cur_embed)

                cur_embed = discord.Embed(
                    title="Shop",
                    colour=discord.Colour.green(),
                )

            price = DataManager.get("economy", "items")[item]["buy price"]
            description = DataManager.get("economy", "items")[item]["description"]
            emoji = DataManager.get("economy", "items")[item]["emoji"]

            if price != 0:
                if user_data["inventory"] is not None:
                    if item.lower() in user_data["inventory"]:
                        cur_embed.add_field(
                            name=f"{emoji} **{item.title()}**"
                            + f" ({json.loads(user_data['inventory'])[item.lower()]}) - {price} 🪙",
                            value=f"{description}",
                            inline=False,
                        )
                else:
                    cur_embed.add_field(
                        name=f"{emoji} **{item.title()}**" + f" - {price} 🪙",
                        value=f"{description}",
                        inline=False,
                    )
            else:
                pass

        embeds.append(cur_embed)

        await Paginator.Simple().paginate(interaction, embeds)

    async def item_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        shop_items = DataManager.get("economy", "shop items").keys()

        return [
            app_commands.Choice(name=item, value=item)
            for item in shop_items
            if item.lower().startswith(current.lower()) or len(current) < 1
        ]

    @app_commands.command(name="buy_item", description="Buy an item")
    @app_commands.autocomplete(item=item_autocomplete)
    @app_commands.checks.cooldown(1, 15, key=lambda i: (i.user.id))
    @app_commands.describe(
        item="The item you want to buy",
        amount="The amount of the item you want to buy (defaults to 1)",
    )
    async def buy_item(
        self, interaction: discord.Interaction, item: str, amount: int = 1
    ):
        if amount <= 0:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You can't buy 0 or a negative amount of items",
                    colour=discord.Colour.red(),
                )
            )

        shop_items = DataManager.get("economy", "shop items")

        if item.lower() in shop_items:
            price = shop_items[item.lower()]["price"]
        else:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> Can't buy that item, because it doesn't exist",
                    colour=discord.Colour.red(),
                )
            )
        user_data = await DataManager.get_user_data(interaction.user.id)
        economy_items = DataManager.get("economy", "items")

        if (int(amount) * price) > user_data["balance"]:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You dont have enough 🪙 to buy that item",
                    colour=discord.Colour.red(),
                )
            )

        if item.lower() not in DataManager.get("economy", "shop items"):
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> Can't buy that item, because it doesn't exist",
                    colour=discord.Colour.red(),
                )
            )

        await DataManager.edit_user_data(
            interaction.user.id, "balance", user_data["balance"] - (int(amount) * price)
        )
        await DataManager.edit_user_inventory(
            interaction.user.id, item.lower(), +int(amount)
        )
        await interaction.response.send_message(
            embed=discord.Embed(
                description=f"{interaction.user.mention} Bought {amount} **{economy_items[item.lower()]["emoji"]} {string.capwords(item.lower())}** and paid **{(int(amount) * price)}** 🪙",
                colour=discord.Colour.from_rgb(43, 45, 49),
            )
            .set_author(
                name=f"Successful {string.capwords(item.lower())} Purchase",
                icon_url=interaction.user.display_avatar,
            )
            .set_footer(text="Thank you for your purchase!")
        )

    async def items_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        items = DataManager.get("economy", "items").keys()

        return [
            app_commands.Choice(name=item, value=item)
            for item in items
            if item.lower().startswith(current.lower()) or len(current) < 1
        ]

    @app_commands.command(name="item", description="View the description of an item")
    @app_commands.autocomplete(item=items_autocomplete)
    @app_commands.checks.cooldown(1, 15, key=lambda i: (i.user.id))
    @app_commands.describe(item="The item you want to view")
    async def item(self, interaction: discord.Interaction, item: str):
        if item not in DataManager.get("economy", "items"):
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> Can't find that item, because it doesn't exist",
                    colour=discord.Colour.red(),
                )
            )

        user_data = await DataManager.get_user_data(interaction.user.id)
        item1 = DataManager.get("economy", "items")[item.lower()]
        emoji = self.bot.get_emoji(item1["emoji_id"])
        whole_balance = user_data["balance"] + user_data["bank"]
        user_inv = user_data["inventory"]
        economy_items = DataManager.get("economy", "items")
        for item_owned in json.loads(user_inv):
            whole_balance += (
                economy_items[item.lower()]["sell price"] * json.loads(user_inv)[item_owned]
            )

        if user_inv is not None:
            inv = json.loads(user_inv)
            if item.lower() in inv:
                itemsowned = inv[item.lower()]
            else:
                itemsowned = 0
        else:
            itemsowned = 0

        if whole_balance != 0:
            percentage_of_net = (itemsowned * item1["sell price"]) / whole_balance * 100
        else:
            percentage_of_net = 0

        embed = discord.Embed(
            title=f"{item1['name']}",
            description=f"> {item1['description']} \n\n"
            f"You own **{itemsowned}** "
            + (
                f"({percentage_of_net:.1f}% of your net worth) \n"
                if percentage_of_net > 0
                else "\n"
            )
            + f"Sell Value: {item1['sell price']} 🪙\n"
            + (
                f"Shop Value: {item1['buy price']} 🪙"
                if item1["buy price"] != 0
                else "Can not be bought from the shop"
            ),
            colour=discord.Colour.from_rgb(15, 255, 255),
            url="https://github.com/Majestic-dev/Tester69",
        )

        embed.set_footer(text=item1["type"])
        embed.set_thumbnail(url=emoji.url)

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(economy(bot))
