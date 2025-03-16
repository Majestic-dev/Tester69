import json
from typing import Optional

import datetime
import discord
from discord import app_commands
from discord.ext import commands

from utils import DataManager, Paginator


async def calculate_remaining_xp(level: int, xp: int) -> str:
    with open("data/mine/levels.json", "r") as f:
        levels = json.load(f)["levels"]

    required_xp = levels[str(level + 1)]["requiredXP"]
    remaining_xp = required_xp - xp

    return f"{required_xp-remaining_xp}/{required_xp}"


async def find_user_level(user_id: int):
    user_data = await DataManager.get_user_data(user_id)
    if user_data["mining_xp"] == None:
        return 0
    levels = DataManager.get("levels", "levels")
    for level in levels:
        required_xp = levels[level]["requiredXP"]
        if user_data["mining_xp"] < required_xp:
            return int(level) - 1
        elif user_data["mining_xp"] == required_xp:
            return int(level)
    return 50

class personal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="profile", description="View an user's profile")
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    @app_commands.describe(
        user="The user you want to check the profile of (yours if no user is provided)"
    )
    async def profile(
        self, interaction: discord.Interaction, user: Optional[discord.User] = None
    ):
        if user == None:
            user = interaction.user

        user_data = await DataManager.get_user_data(user.id)
        if user_data["inventory"] is not None:
            inventory = json.loads(user_data["inventory"])
        else:
            inventory = {}

        items = DataManager.get("economy", "items")
        net = user_data["balance"] + user_data["bank"]

        for item in inventory:
            if item in items:
                net += items[item]["sell price"] * inventory[item]

        if user_data["cooldowns"] is not None:
            cooldowns = json.loads(user_data["cooldowns"])
        else:
            cooldowns = {}

        remaining_cooldowns = []

        for cooldown in cooldowns:
            if cooldowns[cooldown] > discord.utils.utcnow().isoformat():
                end_date = datetime.datetime.strptime(
                    cooldowns[cooldown], "%Y-%m-%dT%H:%M:%S.%f%z"
                )
                remaining_cooldowns.append(
                    f"{cooldown.title()} - Ends {discord.utils.format_dt(end_date, style='R')}"
                )

        embed = discord.Embed(
            title=f"{user}",
            url="https://github.com/Majestic-dev/Tester69",
        ).set_thumbnail(url=user.display_avatar)

        level = await find_user_level(user.id)
        remaining_xp = await calculate_remaining_xp(level, user_data["mining_xp"])

        embed.add_field(
            name="Mining Level",
            value=f"Level: `{level}`\nExperience: `{remaining_xp}`",
        )

        embed.add_field(
            name="Wealth",
            value=f"Wallet: `{user_data['balance']} 🪙`\nBank: `{user_data['bank']} 🪙`\nNet: `{net} 🪙`",
        )

        embed.add_field(
            name="Inventory",
            value=f"Unique Items: `{len(inventory)}`\nTotal Items: `{sum(inventory.values())}`\nWorth: `{net - user_data['balance'] - user_data['bank']} 🪙`",
        )

        embed.add_field(
            name="Cooldowns",
            value=f"{"\n".join(remaining_cooldowns) if remaining_cooldowns else 'No active cooldowns'}",
        )

        await interaction.response.send_message(embed=embed)
    
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
            for item, count in items[i : i + 10]:
                name = f"{DataManager.get('economy', 'items')[item.lower()]['emoji']} {item} - {count}"
                inv_embed.add_field(
                    name=f"{name}",
                    value=f"{DataManager.get('economy', 'items')[item.lower()]['type']}",
                    inline=False,
                )
            inv_embed.set_author(
                name=interaction.user.name
                + "'s inventory"
                + f" page {i//10 + 1}/"
                + str(len(items) // 10 + 1),
                icon_url=interaction.user.display_avatar,
            )
            embeds.append(inv_embed)

        await Paginator.Simple().paginate(interaction, embeds)