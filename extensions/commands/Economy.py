import random
from datetime import datetime, timedelta
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from utils import DataManager


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

        self.fish_cooldown = {}
        self.hunt_cooldown = {}
        self.hourly_cooldown = {}
        self.daily_cooldown = {}
        self.monthly_cooldown = {}

    @commands.command(name="add", description="Add set amount of coins to your balance")
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
                        f'<:white_checkmark:1096793014287995061> Added {amount} :coin: to your balance. Your new balance is {user_data["balance"]} :coin:'
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
                    f'<:white_checkmark:1096793014287995061> Added {amount} :coin: to {member.name}\'s balance. Their new balance is {user_data["balance"]} :coin:'
                ),
                colour=discord.Colour.green(),
            )
        )

    @commands.command(
        name="subtract", description="Subtract set amount of coins from your balance"
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
                        f'<:white_checkmark:1096793014287995061> Removed {amount} :coin: from your balance. Your new balance is {user_data["balance"]} :coin:'
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
                    f'<:white_checkmark:1096793014287995061> Removed {amount} :coin: from {member.name}\'s balance. Their new balance is {user_data["balance"]} :coin:'
                ),
                colour=discord.Colour.green(),
            )
        )

    @app_commands.command(name="balance", description="Check your coin balance")
    async def balance(
        self, interaction: discord.Interaction, user: Optional[discord.User] = None
    ):
        if user == None:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Balance",
                    description=(
                        f'Your balance is {DataManager.get_user_data(interaction.user.id)["balance"]} coins'
                    ),
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.green(),
                )
            )
        else:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Balance",
                    description=(
                        f'{user.name}\'s balance is {DataManager.get_user_data(user.id)["balance"]} coins'
                    ),
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.green(),
                )
            )

    @app_commands.command(name="hunt", description="Hunt for some loot")
    async def hunt(self, interaction: discord.Interaction):
        if (
            interaction.user.id in self.hunt_cooldown
            and self.hunt_cooldown[interaction.user.id] > datetime.utcnow()
            and interaction.user.id not in DataManager.get("config", "global_whitelist")
        ):
            remaining = self.hunt_cooldown[interaction.user.id]

            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Cooldown",
                    description=(
                        f"Your cooldown will end <t:{int(remaining.timestamp())}:R>"
                    ),
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.orange(),
                )
            )

        item_name, _ = random_choice_from_dict(DataManager.get("economy", "hunt_items"))
        DataManager.edit_user_inventory(interaction.user.id, item_name, 1)

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Item Caught",
                description=(f"You hunted down a {item_name}!"),
                timestamp=datetime.utcnow(),
                colour=discord.Colour.green(),
            )
        )

        self.hunt_cooldown[interaction.user.id] = datetime.utcnow() + timedelta(
            minutes=10
        )

    @app_commands.command(name="fish", description="Fish for some loot")
    async def fish(self, interaction: discord.Interaction):
        if (
            interaction.user.id in self.fish_cooldown
            and self.fish_cooldown[interaction.user.id] > datetime.utcnow()
            and interaction.user.id not in DataManager.get("config", "global_whitelist")
        ):
            remaining = self.fish_cooldown[interaction.user.id]

            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Cooldown",
                    description=(
                        f"Your cooldown will end <t:{int(remaining.timestamp())}:R>"
                    ),
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.orange(),
                )
            )

        item_name, _ = random_choice_from_dict(DataManager.get("economy", "fish_items"))
        DataManager.edit_user_inventory(interaction.user.id, item_name, 1)

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Item Caught",
                description=(f"You caught a {item_name}!"),
                timestamp=datetime.utcnow(),
                colour=discord.Colour.green(),
            )
        )

        self.fish_cooldown[interaction.user.id] = datetime.utcnow() + timedelta(
            minutes=10
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

    @app_commands.command(name="sell", description="Sell your loot for coins")
    @app_commands.autocomplete(item=item_autocomplete)
    async def sell(self, interaction: discord.Interaction, item: str):
        user_data = DataManager.get_user_data(interaction.user.id)

        if item.lower() not in user_data["inventory"]:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="No Item",
                    description="You don't have any of that item",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.orange(),
                )
            )

        if user_data["inventory"][item.lower()] <= 0:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="No Item",
                    description="You don't have any of that item",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.orange(),
                )
            )

        if item.lower() not in DataManager.get("economy", "sell_prices"):
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Can't Sell",
                    description="I can't sell that item, because it doesn't exist",
                    timestamp=datetime.utcnow(),
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
                description=(f"You sold a {item} for {price} coins!"),
                timestamp=datetime.utcnow(),
                colour=discord.Colour.green(),
            )
        )

    @app_commands.command(
        name="rob", description="Rob the mentioned user out of their coins"
    )
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
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.orange(),
                )
            )
        elif victim_balance == 0:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="This User Does Not Have Any Coins!",
                    description=f"You can't rob <@{victim_id}> since they do not have any coins to rob!",
                    timestamp=datetime.utcnow(),
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
                    description=f"Successfully robbed <@{user.id}> {cash} coins",
                    timestamp=datetime.utcnow(),
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
                timestamp=datetime.utcnow(),
                colour=discord.Colour.red(),
            )
        )

    @app_commands.command(
        name="hourly", description="Gain 100 coins every time you use this command"
    )
    async def hourly(self, interaction: discord.Interaction):
        if (
            interaction.user.id in self.hourly_cooldown
            and self.hourly_cooldown[interaction.user.id] > datetime.utcnow()
            and interaction.user.id not in DataManager.get("config", "global_whitelist")
        ):
            remaining = self.hourly_cooldown[interaction.user.id]

            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Cooldown",
                    description=(
                        f"Your cooldown will end <t:{int(remaining.timestamp())}:R>"
                    ),
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.orange(),
                )
            )

        user_data = DataManager.get_user_data(interaction.user.id)
        DataManager.edit_user_data(
            interaction.user.id, "balance", user_data["balance"] + 10
        )

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Hourly Pay",
                description="You received 10 coins!",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.green(),
            )
        )

        self.hourly_cooldown[interaction.user.id] = datetime.utcnow() + timedelta(
            hours=1
        )

    @app_commands.command(
        name="daily", description="Gain 1000 coins every time you use this command"
    )
    async def daily(self, interaction: discord.Interaction):
        if (
            interaction.user.id in self.daily_cooldown
            and self.daily_cooldown[interaction.user.id] > datetime.utcnow()
            and interaction.user.id not in DataManager.get("config", "global_whitelist")
        ):
            remaining = self.daily_cooldown[interaction.user.id]

            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Cooldown",
                    description=(
                        f"Your cooldown will end <t:{int(remaining.timestamp())}:R>"
                    ),
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.orange(),
                )
            )

        user_data = DataManager.get_user_data(interaction.user.id)
        DataManager.edit_user_data(
            interaction.user.id, "balance", user_data["balance"] + 100
        )

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Daily Pay",
                description="You received 100 coins!",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.green(),
            )
        )

        self.daily_cooldown[interaction.user.id] = datetime.utcnow() + timedelta(
            hours=24
        )

    @app_commands.command(
        name="monthly", description="Gain 20000 coins every time you use the command"
    )
    async def monthly(self, interaction: discord.Interaction):
        if (
            interaction.user.id in self.monthly_cooldown
            and self.monthly_cooldown[interaction.user.id] > datetime.utcnow()
            and interaction.user.id not in DataManager.get("config", "global_whitelist")
        ):
            remaining = self.monthly_cooldown[interaction.user.id]

            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Cooldown",
                    description=(
                        f"Your cooldown will end <t:{int(remaining.timestamp())}:R>"
                    ),
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.orange(),
                )
            )

        user_data = DataManager.get_user_data(interaction.user.id)
        DataManager.edit_user_data(
            interaction.user.id, "balance", user_data["balance"] + 3000
        )

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Monthly Pay",
                description="You received 3000 coins!",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.green(),
            )
        )

        self.monthly_cooldown[interaction.user.id] = datetime.utcnow() + timedelta(
            hours=720
        )

    @app_commands.command(name="inventory", description="See your inventory")
    async def inventory(self, interaction: discord.Interaction):
        user_data = DataManager.get_user_data(interaction.user.id)

        inv_embed = discord.Embed(
            title="Inventory",
            timestamp=datetime.utcnow(),
            colour=discord.Colour.green(),
        )

        for item, count in user_data["inventory"].items():
            inv_embed.add_field(name=item, value=count, inline=True)

        if len(inv_embed.fields) == 0:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Empty Inventory",
                    description="You don't have any items in your inventory",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.orange(),
                )
            )

        await interaction.response.send_message(embed=inv_embed)

    @app_commands.command(
        name="devskip", description="Skip all cooldowns of the mentioned user"
    )
    @commands.is_owner()
    async def devskip(self, interaction: discord.Interaction, user: discord.User):
        skip = discord.Embed(
            title="Cooldown Skipped",
            timestamp=datetime.utcnow(),
            colour=discord.Colour.green(),
        )

        if user.id in self.fish_cooldown:
            self.fish_cooldown.pop(user.id)
            skip.add_field(name="Fishing cooldown", value="Skipped", inline=False)

        if user.id in self.hourly_cooldown:
            self.hourly_cooldown.pop(user.id)
            skip.add_field(name="Hourly cooldown", value="Skipped", inline=False)

        if user.id in self.hunt_cooldown:
            self.hunt_cooldown.pop(user.id)
            skip.add_field(name="Hunting cooldown", value="Skipped", inline=False)

        if user.id in self.monthly_cooldown:
            self.monthly_cooldown.pop(user.id)
            skip.add_field(name="Monthly cooldown", value="Skipped", inline=False)

        if user.id in self.yearly_cooldown:
            self.yearly_cooldown.pop(user.id)
            skip.add_field(name="Yearly cooldown", value="Skipped", inline=True)

        if len(skip.fields) == 0:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="No Cooldowns",
                    description=(f"{user.name} doesn't have any active cooldowns"),
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.orange(),
                )
            )

        await interaction.response.send_message(embed=skip)


async def setup(bot: commands.Bot):
    await bot.add_cog(Economy(bot))
