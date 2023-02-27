import random
from datetime import datetime, timedelta

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


class Economy(commands.GroupCog, group_name="economy"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.fish_cooldown = {}
        self.hunt_cooldown = {}
        self.hourly_cooldown = {}
        self.monthly_cooldown = {}
        self.yearly_cooldown = {}

    @app_commands.command(name="balance", description="Check your coin balance")
    async def balance(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Balance",
                description=(
                    f'Your balance is {DataManager.get_user_data(interaction.user.id)["balance"]} coins'
                ),
                timestamp=datetime.now(),
                colour=discord.Colour.green(),
            )
        )

    @app_commands.command(
        name="add", description="Add set amount of coins to your balance"
    )
    @commands.is_owner()
    async def add(
        self,
        interaction: discord.Interaction,
        amount: int,
    ):
        user_data = DataManager.get_user_data(interaction.user.id)
        DataManager.edit_user_data(
            interaction.user.id, "balance", user_data["balance"] + amount
        )

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Added Coins",
                description=(
                    f'Added {amount} coins to your balance. Your new balance is {user_data["balance"]}'
                ),
                timestamp=datetime.now(),
                colour=discord.Colour.green(),
            )
        )

    @app_commands.command(
        name="subtract", description="Subtract set amount of coins from your balance"
    )
    @commands.is_owner()
    async def subtract(
        self,
        interaction: discord.Interaction,
        amount: int,
    ):
        user_data = DataManager.get_user_data(interaction.user.id)

        if user_data["balance"] - amount < 0:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Coin Subtraction Failed",
                    description=(
                        f'You do not have enough coins. Your balance is {user_data["balance"]}, after the subtraction you would have {user_data["balance"] - amount}.'
                    ),
                    timestamp=datetime.now(),
                    colour=discord.Colour.red(),
                )
            )

        DataManager.edit_user_data(
            interaction.user.id, "balance", user_data["balance"] - amount
        )

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Coin Subtraction Succeeded",
                description=(
                    f'Subtracted {amount} from your balance. Your new balance is {user_data["balance"] - amount}'
                ),
                timestamp=datetime.now(),
                colour=discord.Color.green(),
            )
        )

    @app_commands.command(name="hunt", description="Hunt for some loot")
    async def hunt(self, interaction: discord.Interaction):
        if (
            interaction.user.id in self.hunt_cooldown
            and self.hunt_cooldown[interaction.user.id] > datetime.now()
            and interaction.user.id not in DataManager.get("config", "whitelist")
        ):
            remaining = self.hunt_cooldown[interaction.user.id]

            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Cooldown",
                    description=(
                        f"Your cooldown will end <t:{int(remaining.timestamp())}:R>"
                    ),
                    timestamp=datetime.now(),
                    colour=discord.Colour.orange(),
                )
            )

        item_name, _ = random_choice_from_dict(DataManager.get("economy", "hunt_items"))
        DataManager.edit_user_inventory(interaction.user.id, item_name, 1)

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Item Caught",
                description=(f"You hunted down a {item_name}!"),
                timestamp=datetime.now(),
                colour=discord.Colour.green(),
            )
        )

        self.hunt_cooldown[interaction.user.id] = datetime.now() + timedelta(minutes=10)

    @app_commands.command(name="fish", description="Fish for some loot")
    async def fish(self, interaction: discord.Interaction):
        if (
            interaction.user.id in self.fish_cooldown
            and self.fish_cooldown[interaction.user.id] > datetime.now()
            and interaction.user.id not in DataManager.get("config", "whitelist")
        ):
            remaining = self.fish_cooldown[interaction.user.id]

            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Cooldown",
                    description=(
                        f"Your cooldown will end <t:{int(remaining.timestamp())}:R>"
                    ),
                    timestamp=datetime.now(),
                    colour=discord.Colour.orange(),
                )
            )

        item_name, _ = random_choice_from_dict(DataManager.get("economy", "fish_items"))
        DataManager.edit_user_inventory(interaction.user.id, item_name, 1)

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Item Caught",
                description=(f"You caught a {item_name}!"),
                timestamp=datetime.now(),
                colour=discord.Colour.green(),
            )
        )

        self.fish_cooldown[interaction.user.id] = datetime.now() + timedelta(minutes=10)

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
                    description="You don't have any of that item.",
                    timestamp=datetime.now(),
                    colour=discord.Colour.orange(),
                )
            )

        if user_data["inventory"][item.lower()] <= 0:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="No Item",
                    description="You don't have any of that item.",
                    timestamp=datetime.now(),
                    colour=discord.Colour.orange(),
                )
            )

        if item.lower() not in DataManager.get("economy", "sell_prices"):
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Can't Sell",
                    description="I can't sell that item, because it doesn't exist",
                    timestamp=datetime.now(),
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
                timestamp=datetime.now(),
                colour=discord.Colour.green(),
            )
        )

    @app_commands.command(
        name="hourly", description="Gain 10 coins every time you use this command"
    )
    async def hourly(self, interaction: discord.Interaction):
        if (
            interaction.user.id in self.hourly_cooldown
            and self.hourly_cooldown[interaction.user.id] > datetime.now()
            and interaction.user.id not in DataManager.get("config", "whitelist")
        ):
            remaining = self.hourly_cooldown[interaction.user.id]

            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Cooldown",
                    description=(
                        f"Your cooldown will end <t:{int(remaining.timestamp())}:R>"
                    ),
                    timestamp=datetime.now(),
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
                timestamp=datetime.now(),
                colour=discord.Colour.green(),
            )
        )

        self.hourly_cooldown[interaction.user.id] = datetime.now() + timedelta(hours=1)

    @app_commands.command(
        name="monthly", description="Gain 3000 coins every time you use the command"
    )
    async def monthly(self, interaction: discord.Interaction):
        if (
            interaction.user.id in self.monthly_cooldown
            and self.monthly_cooldown[interaction.user.id] > datetime.now()
            and interaction.user.id not in DataManager.get("config", "whitelist")
        ):
            remaining = self.monthly_cooldown[interaction.user.id]

            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Cooldown",
                    description=(
                        f"Your cooldown will end <t:{int(remaining.timestamp())}:R>"
                    ),
                    timestamp=datetime.now(),
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
                timestamp=datetime.now(),
                colour=discord.Colour.green(),
            )
        )

        self.monthly_cooldown[interaction.user.id] = datetime.now() + timedelta(
            hours=720
        )

    @app_commands.command(name="yearly", description="Get 36000 coins every year")
    async def yearly(self, interaction: discord.Interaction):
        if (
            interaction.user.id in self.yearly_cooldown
            and self.yearly_cooldown[interaction.user.id] > datetime.now()
            and interaction.user.id not in DataManager.get("config", "whitelist")
        ):
            remaining = self.yearly_cooldown[interaction.user.id]

            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Cooldown",
                    description=(
                        f"Your cooldown will end <t:{int(remaining.timestamp())}:R>"
                    ),
                    timestamp=datetime.now(),
                    colour=discord.Colour.orange(),
                )
            )

        user_data = DataManager.get_user_data(interaction.user.id)
        DataManager.edit_user_data(
            interaction.user.id, "balance", user_data["balance"] + 36000
        )

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Yearly Pay",
                description="You received 36000 coins!",
                timestamp=datetime.now(),
                colour=discord.Colour.green(),
            )
        )

        self.monthly_cooldown[interaction.user.id] = datetime.now() + timedelta(
            days=365
        )

    @app_commands.command(name="inventory", description="See your inventory")
    async def inventory(self, interaction: discord.Interaction):
        user_data = DataManager.get_user_data(interaction.user.id)

        inv_embed = discord.Embed(
            title="Inventory",
            timestamp=datetime.now(),
            colour=discord.Colour.green(),
        )

        for item, count in user_data["inventory"].items():
            inv_embed.add_field(name=item, value=count, inline=True)

        if len(inv_embed.fields) == 0:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Empty Inventory",
                    description="You don't have any items in your inventory.",
                    timestamp=datetime.now(),
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
            timestamp=datetime.now(),
            colour=discord.Color.green(),
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
                    timestamp=datetime.now(),
                    colour=discord.Color.orange(),
                )
            )

        await interaction.response.send_message(embed=skip)


async def setup(bot: commands.Bot):
    await bot.add_cog(Economy(bot))
