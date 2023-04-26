import random
from datetime import datetime
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from utils import DataManager


class DropDown(discord.ui.Select):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

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
        if self.values[0] == "cash":
            users = DataManager.get_all_users()

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
            lb_embed.timestamp = datetime.utcnow()
            await interaction.response.edit_message(
                content=None, embed=lb_embed, view=DropDownView(bot=self.bot)
            )

        elif self.values[0] == "bank":
            users = DataManager.get_all_users()
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
            lb_embed.timestamp = datetime.utcnow()
            await interaction.response.edit_message(
                embed=lb_embed, view=DropDownView(bot=self.bot)
            )


class DropDownView(discord.ui.View):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

        self.add_item(DropDown(bot=self.bot))


def random_choice_from_dict(d):
    total_chance = sum(item["chance"] for item in d.values())
    rand = random.uniform(0, total_chance)
    for item_name, item_data in d.items():
        if rand < item_data["chance"]:
            return item_name, item_data
        rand -= item_data["chance"]


class Economy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="add", description="Add set amount of 🪙 to your balance")
    async def add(
        self,
        ctx,
        amount: int,
        member: Optional[discord.Member] = None,
    ):
        if self.bot.owner_id != ctx.author.id:
            return await ctx.reply(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You are not the owner of this bot.",
                    colour=discord.Colour.red(),
                )
            )

        if member == None:
            user_data = DataManager.get_user_data(ctx.author.id)
            DataManager.edit_user_data(
                ctx.author.id, "balance", user_data["balance"] + amount
            )
            return await ctx.reply(
                embed=discord.Embed(
                    description=(
                        f'<:white_checkmark:1096793014287995061> Added {amount} 🪙 to your balance. Your new balance is {user_data["balance"]} 🪙'
                    ),
                    colour=discord.Colour.green(),
                )
            )

        else:
            user_data = DataManager.get_user_data(member.id)
        DataManager.edit_user_data(member.id, "balance", user_data["balance"] + amount)
        return await ctx.reply(
            embed=discord.Embed(
                description=(
                    f'<:white_checkmark:1096793014287995061> Added {amount} 🪙 to {member.name}\'s balance. Their new balance is {user_data["balance"]} 🪙'
                ),
                colour=discord.Colour.green(),
            )
        )

    @commands.command(
        name="subtract", description="Subtract set amount of 🪙 from your balance"
    )
    async def subtract(
        self,
        ctx,
        amount: int,
        member: Optional[discord.Member] = None,
    ):
        if self.bot.owner_id != ctx.author.id:
            return await ctx.reply(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You are not the owner of this bot.",
                    colour=discord.Colour.red(),
                )
            )

        user_data = DataManager.get_user_data(ctx.author.id)

        if member == None:
            DataManager.edit_user_data(
                ctx.author.id, "balance", user_data["balance"] - amount
            )
            return await ctx.reply(
                embed=discord.Embed(
                    description=(
                        f'<:white_checkmark:1096793014287995061> Removed {amount} 🪙 from your balance. Your new balance is {user_data["balance"]} 🪙'
                    ),
                    colour=discord.Colour.green(),
                )
            )

        else:
            user_data = DataManager.get_user_data(member.id)
        DataManager.edit_user_data(member.id, "balance", user_data["balance"] - amount)
        return await ctx.reply(
            embed=discord.Embed(
                description=(
                    f'<:white_checkmark:1096793014287995061> Removed {amount} 🪙 from {member.name}\'s balance. Their new balance is {user_data["balance"]} 🪙'
                ),
                colour=discord.Colour.green(),
            )
        )

    @app_commands.command(name="pay", description="Pay someone some 🪙")
    @app_commands.checks.cooldown(1, 600, key=lambda i: (i.guild_id, i.user.id))
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

        user_data = DataManager.get_user_data(interaction.user.id)
        if user_data["balance"] < amount:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You don't have enough 🪙 to pay that amount!",
                    colour=discord.Colour.red(),
                )
            )

        DataManager.edit_user_data(
            interaction.user.id, "balance", user_data["balance"] - amount
        )
        DataManager.edit_user_data(
            user.id, "balance", DataManager.get_user_data(user.id)["balance"] + amount
        )

        await interaction.response.send_message(
            embed=discord.Embed(
                description=f'<:white_checkmark:1096793014287995061> Paid {user.mention} {amount} 🪙. Your new balance is {user_data["balance"]} 🪙',
                colour=discord.Colour.green(),
            )
        )

    @app_commands.command(name="balance", description="Check your 🪙 balance")
    @app_commands.checks.cooldown(1, 20, key=lambda i: (i.guild_id, i.user.id))
    async def balance(
        self, interaction: discord.Interaction, user: Optional[discord.User] = None
    ):
        if user == None:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title=f"{interaction.user}'s Balance",
                    description=(
                        f'**:moneybag: Wallet:** {DataManager.get_user_data(interaction.user.id)["balance"]} 🪙\n**🏦 Bank:** {DataManager.get_user_data(interaction.user.id)["bank"]} 🪙'
                    ),
                    colour=discord.Colour.green(),
                )
            )
        else:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Balance",
                    description=(
                        f'{user.name}\'s balance is {DataManager.get_user_data(user.id)["balance"]} 🪙'
                    ),
                    colour=discord.Colour.green(),
                )
            )

    @app_commands.command(name="hunt", description="Hunt for some loot")
    @app_commands.checks.cooldown(1, 600, key=lambda i: (i.guild_id, i.user.id))
    async def hunt(self, interaction: discord.Interaction):
        item_name, _ = random_choice_from_dict(DataManager.get("economy", "hunt_items"))
        DataManager.edit_user_inventory(interaction.user.id, item_name, 1)

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Item Caught",
                description=(f"You hunted down a {item_name}!"),
                colour=discord.Colour.green(),
            )
        )

    @app_commands.command(name="fish", description="Fish for some loot")
    @app_commands.checks.cooldown(1, 600, key=lambda i: (i.guild_id, i.user.id))
    async def fish(self, interaction: discord.Interaction):
        item_name, _ = random_choice_from_dict(DataManager.get("economy", "fish_items"))
        DataManager.edit_user_inventory(interaction.user.id, item_name, 1)

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Item Caught",
                description=(f"You caught a {item_name}!"),
                colour=discord.Colour.green(),
            )
        )

    async def item_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        user_data = DataManager.get_user_data(interaction.user.id)
        items_in_inventory = list(user_data["inventory"].keys())

        return [
            app_commands.Choice(name=item, value=item)
            for item in items_in_inventory
            if item.lower().startswith(current.lower())
            or len(current) < 2
            and user_data["inventory"][item] > 0
        ]

    @app_commands.command(name="sell", description="Sell your loot for 🪙")
    @app_commands.autocomplete(item=item_autocomplete)
    @app_commands.checks.cooldown(1, 60, key=lambda i: (i.guild_id, i.user.id))
    async def sell(self, interaction: discord.Interaction, item: str):
        user_data = DataManager.get_user_data(interaction.user.id)

        if item.lower() not in user_data["inventory"]:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="No Item",
                    description="You don't have any of that item",
                    colour=discord.Colour.orange(),
                )
            )

        if user_data["inventory"][item.lower()] <= 0:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="No Item",
                    description="You don't have any of that item",
                    colour=discord.Colour.orange(),
                )
            )

        if item.lower() not in DataManager.get("economy", "sell_prices"):
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Can't Sell",
                    description="I can't sell that item, because it doesn't exist",
                    colour=discord.Colour.red(),
                )
            )

        price = DataManager.get("economy", "sell_prices")[item.lower()]
        DataManager.edit_user_data(
            interaction.user.id, "balance", user_data["balance"] + price
        )
        DataManager.edit_user_inventory(interaction.user.id, item.lower(), -1)

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Item Sold",
                description=(f"You sold a {item} for {price} 🪙!"),
                colour=discord.Colour.green(),
            )
        )

    @app_commands.command(
        name="rob", description="Rob the mentioned user out of their 🪙"
    )
    @app_commands.checks.cooldown(1, 3600, key=lambda i: (i.guild_id, i.user.id))
    async def rob(self, interaction: discord.Interaction, user: discord.User):
        robber_data = DataManager.get_user_data(interaction.user.id)
        robber_id = interaction.user.id
        robber_balance = DataManager.get_user_data(interaction.user.id)["balance"]
        victim_id = user.id
        victim_balance = DataManager.get_user_data(user.id)["balance"]

        if interaction.user.id == user.id:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="You Can Not Rob Yourself!",
                    description="You can't rob yourself, try mentioning another user",
                    colour=discord.Colour.orange(),
                )
            )
        elif victim_balance == 0:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="This User Does Not Have Any 🪙!",
                    description=f"You can't rob <@{victim_id}> since they do not have any 🪙 to rob!",
                    colour=discord.Colour.orange(),
                )
            )
        successfulrob = random.choices([True, False])[0]
        if successfulrob:
            percentage = random.randint(10, 75) / 100
            cash = int(victim_balance * percentage)
            victim_data = DataManager.get_user_data(victim_id)
            DataManager.edit_user_data(
                victim_id, "balance", victim_data["balance"] - cash
            )
            DataManager.edit_user_data(
                robber_id, "balance", robber_data["balance"] + cash
            )

            return await interaction.response.send_message(
                embed=discord.Embed(
                    title=f"Rob Successful",
                    description=f"Successfully robbed <@{user.id}> {cash} 🪙",
                    colour=discord.Colour.green(),
                )
            )

        percentage = random.randint(10, 33) / 100
        cash = int(robber_balance * percentage)
        DataManager.edit_user_data(robber_id, "balance", robber_data["balance"] - cash)
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Rob Unsuccessful",
                description=f"Failed to rob <@{user.id}>",
                colour=discord.Colour.red(),
            )
        )

    @app_commands.command(
        name="hourly", description="Gain 100 🪙 every time you use this command"
    )
    @app_commands.checks.cooldown(1, 3600, key=lambda i: (i.guild_id, i.user.id))
    async def hourly(self, interaction: discord.Interaction):
        user_data = DataManager.get_user_data(interaction.user.id)
        DataManager.edit_user_data(
            interaction.user.id, "balance", user_data["balance"] + 100
        )

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Hourly Pay",
                description="You received 100 🪙!",
                colour=discord.Colour.green(),
            )
        )

    @app_commands.command(
        name="daily", description="Gain 1000 🪙 every time you use this command"
    )
    @app_commands.checks.cooldown(1, 86400, key=lambda i: (i.guild_id, i.user.id))
    async def daily(self, interaction: discord.Interaction):
        user_data = DataManager.get_user_data(interaction.user.id)
        DataManager.edit_user_data(
            interaction.user.id, "balance", user_data["balance"] + 1000
        )

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Daily Pay",
                description="You received 1000 🪙!",
                colour=discord.Colour.green(),
            )
        )

    @app_commands.command(
        name="weekly", description="Gain 5000 🪙 every time you use the command"
    )
    @app_commands.checks.cooldown(1, 604800, key=lambda i: (i.guild_id, i.user.id))
    async def weekly(self, interaction: discord.Interaction):
        user_data = DataManager.get_user_data(interaction.user.id)
        DataManager.edit_user_data(
            interaction.user.id, "balance", user_data["balance"] + 5000
        )

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Weekly Pay",
                description="You received 5000 🪙!",
                colour=discord.Colour.green(),
            )
        )

    @app_commands.command(
        name="monthly", description="Gain 20000 🪙 every time you use the command"
    )
    @app_commands.checks.cooldown(1, 2592000, key=lambda i: (i.guild_id, i.user.id))
    async def monthly(self, interaction: discord.Interaction):
        user_data = DataManager.get_user_data(interaction.user.id)
        DataManager.edit_user_data(
            interaction.user.id, "balance", user_data["balance"] + 20000
        )

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Monthly Pay",
                description="You received 20000 🪙!",
                colour=discord.Colour.green(),
            )
        )

    @app_commands.command(name="inventory", description="See your inventory")
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.guild_id, i.user.id))
    async def inventory(self, interaction: discord.Interaction):
        user_data = DataManager.get_user_data(interaction.user.id)

        inv_embed = discord.Embed(
            title="Inventory",
            colour=discord.Colour.green(),
        )

        for item, count in user_data["inventory"].items():
            inv_embed.add_field(
                name=f"{item} - {count}",
                value="smth goes here (Coming Soon:tm:)",
                inline=False,
            )

        if len(inv_embed.fields) == 0:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Empty Inventory",
                    description="You don't have any items in your inventory",
                    colour=discord.Colour.orange(),
                )
            )

        inv_embed.set_author(
            name=interaction.user.name + "'s inventory",
            icon_url=interaction.user.display_avatar,
        )
        await interaction.response.send_message(embed=inv_embed)

    @app_commands.command(name="deposit", description="Deposit money into your bank")
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.guild_id, i.user.id))
    async def deposit(self, interaction: discord.Interaction, amount: int):
        user_data = DataManager.get_user_data(interaction.user.id)

        if amount > user_data["balance"]:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Not Enough Money",
                    description="You do not have enough money to deposit",
                    colour=discord.Colour.orange(),
                )
            )

        DataManager.edit_user_data(
            interaction.user.id, "balance", user_data["balance"] - amount
        )
        DataManager.edit_user_data(
            interaction.user.id, "bank", user_data["bank"] + amount
        )

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Deposit Successful",
                description=f"Successfully deposited {amount} 🪙 into your bank",
                colour=discord.Colour.green(),
            )
        )

    @app_commands.command(name="withdraw", description="Withdraw money from your bank")
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.guild_id, i.user.id))
    async def withdraw(self, interaction: discord.Interaction, amount: int):
        user_data = DataManager.get_user_data(interaction.user.id)

        if amount > user_data["bank"]:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Not Enough Money",
                    description="You do not have enough money to withdraw",
                    colour=discord.Colour.orange(),
                )
            )

        DataManager.edit_user_data(
            interaction.user.id, "balance", user_data["balance"] + amount
        )
        DataManager.edit_user_data(
            interaction.user.id, "bank", user_data["bank"] - amount
        )

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Withdraw Successful",
                description=f"Successfully withdrew {amount} 🪙 from your bank",
                colour=discord.Colour.green(),
            )
        )

    @app_commands.command(
        name="leaderboard", description="See the top 10 richest people"
    )
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.choices(
        choices=[
            app_commands.Choice(name="💸 Cash", value="cash"),
            app_commands.Choice(name="🏦 Bank", value="bank"),
        ]
    )
    async def leaderboard(
        self, interaction: discord.Interaction, choices: app_commands.Choice[str]
    ):
        view = DropDownView(bot=self.bot)

        if choices.value == "cash":
            users = DataManager.get_all_users()

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
            lb_embed.timestamp = datetime.utcnow()
            await interaction.response.send_message(embed=lb_embed, view=view)

        elif choices.value == "bank":
            users = DataManager.get_all_users()

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
            lb_embed.timestamp = datetime.utcnow()
            await interaction.response.send_message(embed=lb_embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(Economy(bot))
