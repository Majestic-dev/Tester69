from typing import Optional

import discord

from discord import app_commands
from discord.ext import commands

from utils import data_manager, is_owner, UserData


class add(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @app_commands.command(name="add_balance", description="Add set amount of 🪙 to your balance")
    @app_commands.check(is_owner)
    @app_commands.describe(
        amount="The amount you want to add to someone's balance",
        member="The user whose balance you want to add to"
    )
    async def add_balance(
        self,
        interaction: discord.Interaction,
        amount: int,
        member: Optional[discord.Member] = None,
    ):
        user_data: UserData = await data_manager.get_user_data(
            (member.id) if member else interaction.user.id
        )

        if user_data["balance"] + amount > 92233720368547758071:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description=(
                        f"<:white_cross:1096791282023669860> That's too much! Please try lowering your needed amount"
                    ),
                    colour=discord.Colour.red(),
                )
            )

        await data_manager.edit_user_data(
            (member.id) if member else interaction.user.id,
            "balance",
            user_data["balance"] + amount,
        )
        return await interaction.response.send_message(
            embed=discord.Embed(
                description=(
                    f"<:white_checkmark:1096793014287995061> Added {amount} 🪙 "
                )
                + (
                    f"to {member.mention}'s bank. Their new balance is {user_data["balance"] + amount} 🪙"
                    if member
                    else f"to your bank. Your new balance is {user_data["balance"] + amount} 🪙"
                ),
                colour=discord.Colour.green(),
            )
        )
    
    async def items_autocomplete(
            self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        items = data_manager.get("economy", "items").keys()

        return [
            app_commands.Choice(name=item, value=item)
            for item in items
            if item.lower().startswith(current.lower()) or len(current) < 1
        ]
    
    @app_commands.command(name="add_item", description="Add an item to your inventory")
    @app_commands.check(is_owner)
    @app_commands.autocomplete(item_name=items_autocomplete)
    @app_commands.describe(
        item_name="The item to add to the inventory",
        amount="Amount of the item to add to the inventory",
        member="The user whose inventory to add the item in to"
    )
    async def add_item(
        self,
        interaction: discord.Interaction,
        item_name: str,
        amount: Optional[int] = 1,
        member: Optional[discord.Member] = None,
    ):
        items = data_manager.get("economy", "items")
        if item_name.lower() not in items:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description=(
                        f"<:white_cross:1096791282023669860> {item_name} does not exist"
                    ),
                    colour=discord.Colour.red(),
                )
            )

        if member == None:
            member = interaction.user

        await data_manager.edit_user_inventory(member.id, item_name, amount)

        if member == interaction.user:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description=("<:white_checkmark:1096793014287995061> ")
                    + ("Added " if amount >= 1 else "Removed ")
                    + (f"{abs(amount)} {items[item_name.lower()]["emoji"]} {item_name}")
                    + ("s to your inventory" if amount > 1 else " to your inventory"),
                    colour=discord.Colour.green(),
                )
            )

        else:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description=("<:white_checkmark:1096793014287995061>")
                    + ("Added " if amount >= 1 else "Removed ")
                    + (f"{abs(amount)} {items[item_name.lower()]["emoji"]} {item_name}")
                    + (
                        f"s to {member.mention}'s inventory"
                        if amount > 1
                        else f" to {member.mention}'s inventory"
                    ),
                    colour=discord.Colour.green(),
                )
            )
        
async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(add(bot))