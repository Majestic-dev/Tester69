import os
from typing import Optional

import discord
from discord.ext import commands

from utils import DataManager


class OwnerOnly(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.command(name="add", description="Add set amount of 🪙 to your balance")
    @commands.is_owner()
    async def add(
        self,
        ctx,
        amount: int,
        member: Optional[discord.Member] = None,
    ):
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

    @commands.command(name="addbank", description="Add set amount of 🪙 to your balance")
    @commands.is_owner()
    async def addbank(
        self,
        ctx,
        amount: int,
        member: Optional[discord.Member] = None,
    ):
        if member == None:
            user_data = DataManager.get_user_data(ctx.author.id)
            DataManager.edit_user_data(
                ctx.author.id, "bank", user_data["bank"] + amount
            )
            return await ctx.reply(
                embed=discord.Embed(
                    description=(
                        f'<:white_checkmark:1096793014287995061> Added {amount} 🪙 to your bank. Your new bank balance is {user_data["bank"]} 🪙'
                    ),
                    colour=discord.Colour.green(),
                )
            )

        else:
            user_data = DataManager.get_user_data(member.id)
        DataManager.edit_user_data(member.id, "bank", user_data["bank"] + amount)
        return await ctx.reply(
            embed=discord.Embed(
                description=(
                    f'<:white_checkmark:1096793014287995061> Added {amount} 🪙 to {member.name}\'s bank. Their new bank balance is {user_data["bank"]} 🪙'
                ),
                colour=discord.Colour.green(),
            )
        )

    @commands.command(
        name="subtract", description="Subtract set amount of 🪙 from your balance"
    )
    @commands.is_owner()
    async def subtract(
        self,
        ctx,
        amount: int,
        member: Optional[discord.Member] = None,
    ):
        if member == None:
            user_data = DataManager.get_user_data(ctx.author.id)
            DataManager.edit_user_data(
                ctx.author.id, "balance", user_data["balance"] - amount
            )
            await ctx.reply(
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
        await ctx.reply(
            embed=discord.Embed(
                description=(
                    f'<:white_checkmark:1096793014287995061> Removed {amount} 🪙 from {member.name}\'s balance. Their new balance is {user_data["balance"]} 🪙'
                ),
                colour=discord.Colour.green(),
            )
        )

    @commands.command(
        name="subtractbank", description="Subtract set amount of 🪙 from your balance"
    )
    @commands.is_owner()
    async def subtractbank(
        self, ctx, amount: int, member: Optional[discord.Member] = None
    ):
        user_data = DataManager.get_user_data(ctx.author.id)

        if member == None:
            DataManager.edit_user_data(
                ctx.author.id, "bank", user_data["bank"] - amount
            )
            await ctx.reply(
                embed=discord.Embed(
                    description=(
                        f'<:white_checkmark:1096793014287995061> Removed {amount} 🪙 from your bank. Your new bank balance is {user_data["bank"]} 🪙'
                    ),
                    colour=discord.Colour.green(),
                )
            )

        else:
            user_data = DataManager.get_user_data(member.id)
        DataManager.edit_user_data(member.id, "bank", user_data["bank"] - amount)
        await ctx.reply(
            embed=discord.Embed(
                description=(
                    f'<:white_checkmark:1096793014287995061> Removed {amount} 🪙 from {member.name}\'s bank. Their new bank balance is {user_data["bank"]} 🪙'
                ),
                colour=discord.Colour.green(),
            )
        )

    @commands.command(name="reload", description="Reload the cogs in the bot")
    @commands.is_owner()
    async def reload(self, ctx):
        for root, _, files in os.walk("extensions"):
            for file in files:
                if file.endswith(".py"):
                    await self.bot.reload_extension(
                        root.replace("\\", ".") + "." + file[:-3]
                    )

        await ctx.reply(
            embed=discord.Embed(
                description="<:white_checkmark:1096793014287995061> Reloaded all cogs",
                colour=discord.Colour.green(),
            )
        )
        return await self.bot.tree.sync()


async def setup(bot: commands.Bot):
    await bot.add_cog(OwnerOnly(bot))
