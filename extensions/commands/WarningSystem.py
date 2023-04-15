from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

from utils import DataManager


class WarningSystem(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="warn", description="Warns the mentioned user with a custom warning reason"
    )
    @app_commands.default_permissions(manage_messages=True)
    async def warn(
        self, interaction: discord.Interaction, user: discord.User, *, reason: str
    ):
        if user.id == interaction.user.id:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error",
                    description="You can't warn yourself",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.orange(),
                )
            )

        if interaction.user.top_role.position <= user.top_role.position:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error",
                    description="You can't warn someone with a higher role than you",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.orange(),
                )
            )

        user_id = str(user.id)
        DataManager.register_warning(
            interaction.guild.id,
            user_id,
            f"{reason} - Warned by {interaction.user.name}#{interaction.user.discriminator}",
        )

        return await interaction.response.send_message(
            embed=discord.Embed(
                title="Warning",
                description=(f"{user.name} has been warned for: ```{reason}```"),
                timestamp=datetime.utcnow(),
                colour=discord.Colour.red(),
            )
        )

    @app_commands.command(name="delwarn", description="Deletes the warning by UUID")
    @app_commands.default_permissions(manage_messages=True)
    async def delwarn(self, interaction: discord.Interaction, uuid: str):
        warnings = DataManager.get_guild_data(interaction.guild.id)["warned_users"]

        for user in warnings:
            for index, warn in enumerate(warnings[user]):
                if uuid in warn:
                    warnings[user].pop(index)
                    if len(warnings[user]) <= 0:
                        warnings.pop(user)
                    DataManager.save("guilds")
                    return await interaction.response.send_message(
                        embed=discord.Embed(
                            title="Warning Deleted",
                            description=(f"Deleted warning ```{uuid}```"),
                            timestamp=datetime.utcnow(),
                            colour=discord.Colour.green(),
                        )
                    )

        return await interaction.response.send_message(
            embed=discord.Embed(
                title="Warning Not Found",
                description=(f"Couldn't find warning with the UUID ```{uuid}```"),
                timestamp=datetime.utcnow(),
                colour=discord.Colour.orange(),
            )
        )

    @app_commands.command(
        name="warnings", description="get the warning list of the user"
    )
    @app_commands.default_permissions(manage_messages=True)
    async def warnings(self, interaction: discord.Interaction, member: discord.Member):
        warnings = DataManager.get_guild_data(interaction.guild.id)["warned_users"]

        if len(warnings) == 0:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Warnings",
                    description=f"{member.mention} has no warnings",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.green(),
                )
            )

        e = discord.Embed(
            title="Warnings",
            timestamp=datetime.utcnow(),
            colour=discord.Colour.orange(),
        )

        for user in warnings:
            for warn in warnings[user]:
                for warn_uuid in warn:
                    e.add_field(
                        name=f"UUID: `{warn_uuid}`",
                        value=f"\n{warn[warn_uuid]}",
                        inline=False,
                    )
        e.set_author(name=member.name, icon_url=member.avatar.url)
        await interaction.response.send_message(embed=e)


async def setup(bot: commands.Bot):
    await bot.add_cog(WarningSystem(bot))
