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
            user_data = await DataManager.get_user_data(ctx.author.id)
            await DataManager.edit_user_data(
                ctx.author.id, "balance", user_data["balance"] + amount
            )
            return await ctx.reply(
                embed=discord.Embed(
                    description=(
                        f'<:white_checkmark:1096793014287995061> Added {amount} 🪙 to your balance. Your new balance is {user_data["balance"] + amount} 🪙'
                    ),
                    colour=discord.Colour.green(),
                )
            )

        else:
            user_data = await DataManager.get_user_data(member.id)
            await DataManager.edit_user_data(
                member.id, "balance", user_data["balance"] + amount
            )
            return await ctx.reply(
                embed=discord.Embed(
                    description=(
                        f'<:white_checkmark:1096793014287995061> Added {amount} 🪙 to {member.name}\'s balance. Their new balance is {user_data["balance"] + amount} 🪙'
                    ),
                    colour=discord.Colour.green(),
                )
            )

    @commands.command(
        name="addbank", description="Add set amount of 🪙 to your bank balance"
    )
    @commands.is_owner()
    async def addbank(
        self,
        ctx,
        amount: int,
        member: Optional[discord.Member] = None,
    ):
        if member == None:
            user_data = await DataManager.get_user_data(ctx.author.id)
            await DataManager.edit_user_data(
                ctx.author.id, "bank", user_data["bank"] + amount
            )
            return await ctx.reply(
                embed=discord.Embed(
                    description=(
                        f'<:white_checkmark:1096793014287995061> Added {amount} 🪙 to your bank. Your new bank balance is {user_data["bank"] + amount} 🪙'
                    ),
                    colour=discord.Colour.green(),
                )
            )

        else:
            user_data = await DataManager.get_user_data(member.id)
            await DataManager.edit_user_data(
                member.id, "bank", user_data["bank"] + amount
            )
            return await ctx.reply(
                embed=discord.Embed(
                    description=(
                        f'<:white_checkmark:1096793014287995061> Added {amount} 🪙 to {member.name}\'s bank. Their new bank balance is {user_data["bank"] + amount} 🪙'
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

    @commands.command(name="skipcooldown", description="Skip the cooldown of a command")
    @commands.is_owner()
    async def skipcooldown(
        self, ctx, command: str, member: Optional[discord.Member] = None
    ):
        if member == None:
            if command == "all":
                await DataManager.remove_all_cooldowns(ctx.author.id)
                return await ctx.reply(
                    embed=discord.Embed(
                        description=(
                            f"<:white_checkmark:1096793014287995061> Skipped all cooldowns for {ctx.author.name}"
                        ),
                        colour=discord.Colour.green(),
                    )
                )

            cooldowns = await DataManager.get_user_data(ctx.author.id)["cooldowns"]
            if command not in cooldowns:
                return await ctx.reply(
                    embed=discord.Embed(
                        description=(
                            f"<:error:109679301358805760> {command} command is not on cooldown or does not exist"
                        ),
                        colour=discord.Colour.red(),
                    )
                )

            await DataManager.remove_cooldown(ctx.author.id, command)

            return await ctx.reply(
                embed=discord.Embed(
                    description=(
                        f"<:white_checkmark:1096793014287995061> Skipped cooldown for {command} command"
                    ),
                    colour=discord.Colour.green(),
                )
            )

        else:
            if command == "all":
                await DataManager.remove_all_cooldowns(member.id)
                return await ctx.reply(
                    embed=discord.Embed(
                        description=(
                            f"<:white_checkmark:1096793014287995061> Skipped all cooldowns for {member.name}"
                        ),
                        colour=discord.Colour.green(),
                    )
                )

            cooldowns = await DataManager.get_user_data(member.id)["cooldowns"]
            if command not in cooldowns:
                return await ctx.reply(
                    embed=discord.Embed(
                        description=(
                            f"<:error:109679301358805760> {command} command is not on cooldown or does not exist"
                        ),
                        colour=discord.Colour.red(),
                    )
                )

            await DataManager.remove_cooldown(member.id, command)

            return await ctx.reply(
                embed=discord.Embed(
                    description=(
                        f"<:white_checkmark:1096793014287995061> Skipped cooldown for {command} command for {member.name}"
                    ),
                    colour=discord.Colour.green(),
                )
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(OwnerOnly(bot))
