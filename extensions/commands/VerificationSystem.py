import asyncio
import random
from datetime import datetime
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from utils import DataManager


class VerificationSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="set_verification_channel",
        description="Set the channel where users should send their verification code",
    )
    @app_commands.default_permissions(administrator=True)
    async def set_verification_channel(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        guild_data = DataManager.get_guild_data(interaction.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if logs_channel == None:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="No Logs Channel",
                    description="Please set a channel where all logs will be sent. `/set_logs_channel`",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.orange(),
                )
            )
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Verification Channel Set!",
                description=f"Verification channel set to {channel.mention}",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.green(),
            )
        )

        DataManager.edit_guild_data(
            interaction.guild.id, "verification_channel_id", channel.id
        )

    @app_commands.command(
        name="set_verification_logs_channel",
        description="Set the channel where all verification logs are sent",
    )
    @app_commands.default_permissions(administrator=True)
    async def set_verification_logs_channel(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        guild_data = DataManager.get_guild_data(interaction.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if logs_channel == None:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="No Logs Channel",
                    description="Please set a channel where all logs will be sent. `/set_logs_channel`",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.orange(),
                )
            )
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Verification Logs Channel Set!",
                description=f"Verification logs channel set to {channel.mention}",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.green(),
            )
        )

        DataManager.edit_guild_data(
            interaction.guild.id, "verification_logs_channel_id", channel.id
        )

    @app_commands.command(
        name="set_unverified_role",
        description="Set the unverified role that will be assigned to members when they join",
    )
    @app_commands.default_permissions(administrator=True)
    async def set_verification_role(
        self, interaction: discord.Interaction, role: discord.Role
    ):
        guild_data = DataManager.get_guild_data(interaction.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if logs_channel == None:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="No Logs Channel",
                    description="Please set a channel where all logs will be sent. `/set_logs_channel`",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.orange(),
                )
            )

        await interaction.response.send_message(
            embed=discord.Embed(
                title="New Member Role Set!",
                description=f"All new members will now receive the {role.mention} role",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.green(),
            )
        )

        DataManager.edit_guild_data(interaction.guild.id, "unverified_role_id", role.id)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_data = DataManager.get_guild_data(member.guild.id)

        verification_role = discord.utils.get(
            member.guild.roles,
            id=guild_data["unverified_role_id"],
        )

        if verification_role is None:
            return print("Role couldn't be found")

        await member.add_roles(verification_role)
        dm_channel = await member.create_dm()

        code = str(random.randint(10000, 99999))
        verification_channel = self.bot.get_channel(
            guild_data["verification_channel_id"]
        )
        await dm_channel.send(
            embed=discord.Embed(
                title="Verification",
                description=f"Welcome to the server! Your verification code is: `{code}` please enter it in the <#{verification_channel}>\nYou may cancel this request by typing 'cancel' in <#{verification_channel}>",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.blue(),
            )
        )

        check = lambda m: m.channel == self.bot.get_channel(
            guild_data["verification_channel_id"]
        )

        while True:
            for i in range(3):
                try:
                    message = await self.bot.wait_for(
                        "message", check=check, timeout=300
                    )
                except asyncio.TimeoutError:
                    return await dm_channel.send(
                        embed=discord.Embed(
                            title="Timeout",
                            description=f"You took too long to enter the verification code. Please rejoin the server and try again",
                            timestamp=datetime.utcnow(),
                            colour=discord.Colour.orange(),
                        )
                    )

                if message.content == code:
                    await member.remove_roles(verification_role)
                    await message.delete()
                    await dm_channel.send(
                        embed=discord.Embed(
                            title="Verification Completed!",
                            description=f"{member.mention}, you are now verified!",
                            timestamp=datetime.utcnow(),
                            colour=discord.Colour.green(),
                        )
                    )

                    verification_logs_channel = self.bot.get_channel(
                        guild_data["verification_logs_channel_id"]
                    )

                    await verification_logs_channel.send(
                        embed=discord.Embed(
                            title="Verification Completed!",
                            description=f"{member.mention} has verified themselves!",
                            timestamp=datetime.utcnow(),
                            colour=discord.Colour.green(),
                        )
                    )

                    return

                elif message.content.lower() == "cancel":
                    await dm_channel.send(
                        embed=discord.Embed(
                            title="Verification Cancelled",
                            description=f"Verification cancelled. Please rejoin the server if you'd like to verify yourself",
                            timestamp=datetime.utcnow(),
                            colour=discord.Colour.orange(),
                        )
                    )
                    await message.delete()

                    verification_logs_channel = self.bot.get_channel(
                        guild_data["verification_logs_channel_id"]
                    )

                    await verification_logs_channel.send(
                        embed=discord.Embed(
                            title="Verification Cancelled",
                            description=f"{member.mention} has cancelled their verification",
                            timestamp=datetime.utcnow(),
                            colour=discord.Colour.orange(),
                        )
                    )
                    return
                else:
                    await dm_channel.send(
                        embed=discord.Embed(
                            title="Invalid Code",
                            description=f"Invalid verification code! You have {2-i} attempts remaining",
                            timestamp=datetime.utcnow(),
                            colour=discord.Colour.orange(),
                        )
                    )
                    await message.delete()

            code = str(random.randint(10000, 99999))
            await dm_channel.send(
                embed=discord.Embed(
                    title="Code Reset",
                    description=f"You have used all your attempts. Your new verification code is: {code}",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.red(),
                )
            )
            verification_logs_channel = self.bot.get_channel(
                guild_data["verification_logs_channel_id"]
            )

            await verification_logs_channel.send(
                embed=discord.Embed(
                    title="Code Reset",
                    description=f"{member.mention}'s code was reset",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.red(),
                )
            )


async def setup(bot):
    await bot.add_cog(VerificationSystem(bot))
