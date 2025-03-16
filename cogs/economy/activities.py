import json
import random

import discord
from discord import app_commands
from discord.ext import commands

from utils import DataManager, cooldown_check


class activities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="hunt",
        description="Grab a rifle from the shop and go hunting for some animals",
    )
    async def hunt(self, interaction: discord.Interaction):
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

        if await cooldown_check(
            interaction.user.id,
            "<:white_cross:1096791282023669860> You already went hunting",
            "hunt",
            600,
        ):
            chances = []
            for item in DataManager.get("economy", "hunting items").values():
                chances.append(item["chance"])
            items = list(DataManager.get("economy", "hunting items").keys())
            item_name = random.choices(items, weights=chances, k=1)
            item_emoji = DataManager.get("economy", "items")[item_name[0]]["emoji"]
            user_data = await DataManager.get_user_data(interaction.user.id)

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

        if await cooldown_check(
            interaction.user.id,
            "<:white_cross:1096791282023669860> You already went fishing",
            "fish",
            600,
        ):
            chances = []
            for item in DataManager.get("economy", "fishing items").values():
                chances.append(item["chance"])
            items = list(DataManager.get("economy", "fishing items").keys())
            item_name = random.choices(items, weights=chances, k=1)
            item_emoji = DataManager.get("economy", "items")[item_name[0]]["emoji"]

            await DataManager.edit_user_inventory(interaction.user.id, item_name[0], 1)

            await interaction.response.send_message(
                embed=discord.Embed(
                    description=f"You caught a **{item_emoji} {item_name[0]}**",
                    colour=discord.Colour.green(),
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
                    interaction.user.id, "bank", robber_data["bank"] - cash2
                )
                await interaction.response.send_message(
                    embed=discord.Embed(
                        description=f"<:white_cross:1096791282023669860> You got caught trying to rob <@{user.id}> and had to pay the police {cash2}",
                        colour=discord.Colour.red(),
                    )
                )