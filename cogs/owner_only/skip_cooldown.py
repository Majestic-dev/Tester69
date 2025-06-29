from typing import Optional

import discord
from discord.ext import commands

from utils import data_manager

class skip_cooldown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="skipcooldown", description="Skip the cooldown of a command")
    @commands.is_owner()
    async def skipcooldown(
        self, ctx, command: str, member: Optional[discord.Member] = None
    ):
        if member == None:
            if command == "all":
                await data_manager.remove_cooldown(ctx.author.id, "all")
                return await ctx.reply(
                    embed=discord.Embed(
                        description=(
                            f"<:white_checkmark:1096793014287995061> Skipped all cooldowns"
                        ),
                        colour=discord.Colour.green(),
                    )
                )

            user_data = await data_manager.get_user_data(ctx.author.id)
            if command not in user_data["cooldowns"]:
                return await ctx.reply(
                    embed=discord.Embed(
                        description=(
                            f"<:white_cross:1096791282023669860> {command} command is not on cooldown or does not exist"
                        ),
                        colour=discord.Colour.red(),
                    )
                )

            await data_manager.remove_cooldown(ctx.author.id, command)

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
                await data_manager.remove_cooldown(member.id, "all")
                return await ctx.reply(
                    embed=discord.Embed(
                        description=(
                            f"<:white_checkmark:1096793014287995061> Skipped all cooldowns for {member.mention}"
                        ),
                        colour=discord.Colour.green(),
                    )
                )

            user_data = await data_manager.get_user_data(member.id)
            if command not in user_data["cooldowns"]:
                return await ctx.reply(
                    embed=discord.Embed(
                        description=(
                            f"<:white_cross:1096791282023669860> {command} command is not on cooldown or does not exist"
                        ),
                        colour=discord.Colour.red(),
                    )
                )

            await data_manager.remove_cooldown(member.id, command)

            return await ctx.reply(
                embed=discord.Embed(
                    description=(
                        f"<:white_checkmark:1096793014287995061> Skipped cooldown for {command} command for {member.name}"
                    ),
                    colour=discord.Colour.green(),
                )
            )
        
async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(skip_cooldown(bot))