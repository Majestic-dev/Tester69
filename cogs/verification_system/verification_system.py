import asyncio
import os
import random
from io import BytesIO

import discord
from discord import app_commands
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from utils import data_manager, GuildData


class verification(commands.GroupCog):
    def __init__(self, bot):
        self.bot = bot
        self.buffer = None

    def generate_img(self, code: int, member_id: int) -> None:
        background_colour = (
            random.randint(0, 122),
            random.randint(0, 122),
            random.randint(0, 122),
        )
        text_colour = (
            random.randint(123, 255),
            random.randint(123, 255),
            random.randint(123, 255),
        )
        pos = (
            random.randint(0, 100),
            random.randint(0, 100),
        )
        randomfont = random.choice(os.listdir("fonts"))

        font = ImageFont.truetype(
            font=f"fonts/{randomfont}", size=random.randint(50, 75)
        )
        verification_background = Image.new("RGB", (300, 300), background_colour)
        background = ImageDraw.Draw(verification_background)
        background.text(
            (pos),
            f"{code}",
            fill=(text_colour),
            font=font,
        )
        rotated_image = verification_background.rotate(
            random.randint(-50, 50), expand=True, fillcolor=background_colour
        )
        blurred_image = rotated_image.filter(ImageFilter.GaussianBlur(3))

        for _ in range(round(blurred_image.size[0] * blurred_image.size[1] / 4)):
            blurred_image.putpixel(
                (
                    random.randint(0, blurred_image.size[0] - 1),
                    random.randint(0, blurred_image.size[1] - 1),
                ),
                random.choice([(0, 0, 0), (255, 255, 255)]),
            )

        self.buffer = BytesIO()
        blurred_image.save(self.buffer, "png")
        self.buffer.seek(0)

    @app_commands.command(
        name="disable",
        description="Disable the verification system",
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    async def disable_verification(self, interaction: discord.Interaction):
        guild_data: GuildData = await data_manager.get_guild_data(interaction.guild.id)
        verification_channel: GuildData = await data_manager.get_guild_data(interaction.guild.id)[
            "verification_channel_id"
        ]
        verification_logs_channel: GuildData = await data_manager.get_guild_data(
            interaction.guild.id
        )["verification_logs_channel_id"]
        unverified_role: GuildData = await data_manager.get_guild_data(interaction.guild.id)[
            "unverified_role_id"
        ]

        if (
            guild_data["verification_channel_id"]
            and guild_data["verification_logs_channel_id"]
            and guild_data["unverified_role_id"] == ("disabled")
        ):
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> Verification is already disabled or has not been interacted with for this server",
                    colour=discord.Colour.orange(),
                )
            )

        await interaction.response.send_message(
            embed=discord.Embed(
                description="<:white_checkmark:1096793014287995061> Verification has been disabled for this server",
                colour=discord.Colour.green(),
            )
        )

        await data_manager.edit_guild_data(
            interaction.guild.id, "verification_channel_id", None
        )
        await data_manager.edit_guild_data(
            interaction.guild.id, "verification_logs_channel_id", None
        )
        await data_manager.edit_guild_data(
            interaction.guild.id, "unverified_role_id", None
        )

    @app_commands.command(
        name="setup",
        description="Setup the verification system",
    )
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 60, key=lambda i: (i.guild.id, i.user.id))
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(
        verification_channel="The channel where users will send the verification code",
        verification_logs_channel="The channel where the bot will send the verification logs",
        unverified_role="The role that will be given to the user when they join the server",
    )
    async def verification_setup(
        self,
        interaction: discord.Interaction,
        verification_channel: discord.TextChannel,
        verification_logs_channel: discord.TextChannel,
        unverified_role: discord.Role,
    ):
        verification = discord.Embed(
            description="<:white_checkmark:1096793014287995061> Verification has been setup for this server",
            colour=discord.Colour.green(),
        )
        verification.add_field(
            name="Verification Channel",
            value=f"<#{verification_channel.id}>",
            inline=False,
        )
        verification.add_field(
            name="Verification Logs Channel",
            value=f"<#{verification_logs_channel.id}>",
            inline=False,
        )
        verification.add_field(
            name="Unverified Role", value=f"<@&{unverified_role.id}>", inline=False
        )
        await interaction.response.send_message(embed=verification)

        await data_manager.edit_guild_data(
            interaction.guild.id, "verification_channel_id", verification_channel.id
        )
        await data_manager.edit_guild_data(
            interaction.guild.id,
            "verification_logs_channel_id",
            verification_logs_channel.id,
        )
        await data_manager.edit_guild_data(
            interaction.guild.id, "unverified_role_id", unverified_role.id
        )

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.bot:
            return
        guild_data: GuildData = await data_manager.get_guild_data(member.guild.id)
        welcome_message = guild_data["welcome_message"]
        verification_channel = guild_data["verification_channel_id"]
        verification_logs_channel = guild_data["verification_logs_channel_id"]
        unverified_role = member.guild.get_role(guild_data["unverified_role_id"])

        if (
            verification_channel == None
            and verification_logs_channel == None
            and unverified_role == None
        ):
            if welcome_message != None:
                dm_channel = await member.create_dm()
                if dm_channel:
                    return await dm_channel.send(welcome_message)
                else:
                    return
            return

        else:
            verification_channel = self.bot.get_channel(verification_channel)
            verification_logs_channel = self.bot.get_channel(
                guild_data["verification_logs_channel_id"]
            )

            self.generate_img(code := str(random.randint(11111, 99999)), member.id)

            await member.add_roles(unverified_role)
            dm_channel = await member.create_dm()

            if dm_channel:
                buffer = self.buffer
                await dm_channel.send(
                    f'Please enter the code seen in the image. If the code is too blurry and you can not see it type "reset".\n By verifying yourself you accept the rules of the server you are trying to verify in',
                    file=discord.File(fp=buffer, filename="verification.png"),
                )
            else:
                await verification_channel.send(
                    f"{member.mention} Please enable your direct messages to verify yourself, rejoin once done. Thanks!"
                )
                await asyncio.sleep(30)
                return await message.delete()

        check = (
            lambda m: m.channel == dm_channel
            or m.channel == verification_channel
            and m.author == member
        )
        fail_count = 3

        while fail_count > 0:
            if fail_count == 0:
                break
            try:
                message = await self.bot.wait_for("message", check=check, timeout=300)
            except asyncio.TimeoutError:
                server = member.guild
                invite = await server.text_channels[0].create_invite(
                    max_age=0, max_uses=1, unique=True
                )

                await dm_channel.send(
                    embed=discord.Embed(
                        title="Timeout",
                        description=f"You took too long to enter the verification code. Please rejoin the server and try again: {invite}",
                        colour=discord.Colour.orange(),
                    )
                )

                return await member.kick()

            if message.content == code:
                try:
                    await message.delete()
                    await member.remove_roles(unverified_role)
                except:
                    await member.remove_roles(unverified_role)

                verification_logs_channel = self.bot.get_channel(
                    guild_data["verification_logs_channel_id"]
                )

                await verification_logs_channel.send(
                    embed=discord.Embed(
                        title="Verification Completed!",
                        description=f"{member.mention} has verified themselves!",
                        colour=discord.Colour.green(),
                    )
                )

                await dm_channel.send(
                    embed=discord.Embed(
                        title="Verification Completed!",
                        description=f"You have verified yourself in {member.guild.name}",
                        colour=discord.Colour.green(),
                    )
                )
                if welcome_message != None:
                    if await dm_channel.send(welcome_message):
                        return
                    else:
                        return
                return

            elif message.content.lower() == "cancel":
                return await dm_channel.send(
                    embed=discord.Embed(
                        title="Verification Cancelled",
                        description=f"Verification cancelled. Please rejoin the server if you'd like to verify yourself",
                        colour=discord.Colour.orange(),
                    )
                )

            elif message.content.lower() == "reset":
                self.generate_img(code := str(random.randint(11111, 99999)), member.id)
                buffer = self.buffer
                await dm_channel.send(
                    f'Please enter the code seen in the image. If the code is too blurry and you can not see it type "reset".\n By verifying yourself you accept the rules of the server you are trying to verify in',
                    file=discord.File(fp=buffer, filename="verification.png"),
                )

                await verification_logs_channel.send(
                    embed=discord.Embed(
                        title="Code Reset",
                        description=f"{member.mention}'s code was reset",
                        colour=discord.Colour.red(),
                    )
                )
            else:
                fail_count -= 1
                await dm_channel.send(
                    embed=discord.Embed(
                        title="Invalid Code",
                        description=f"Invalid verification code! You have {fail_count} attempts remaining",
                        colour=discord.Colour.orange(),
                    )
                )

                self.generate_img(code := str(random.randint(11111, 99999)), member.id)
                buffer = self.buffer
                await dm_channel.send(
                    f'Please enter the code seen in the image. If the code is too blurry and you can not see it type "reset".\n By verifying yourself you accept the rules of the server you are trying to verify in',
                    file=discord.File(fp=buffer, filename="verification.png"),
                )

                await verification_logs_channel.send(
                    embed=discord.Embed(
                        title="Code Reset",
                        description=f"{member.mention}'s code was reset",
                        colour=discord.Colour.red(),
                    )
                )

        server = member.guild
        invite = await server.text_channels[0].create_invite(
            max_age=0, max_uses=1, unique=True
        )

        await dm_channel.send(
            embed=discord.Embed(
                description=f"<:white_cross:1096791282023669860> You entered the verification code wrong too many times. Please rejoin the server and try again: {invite}",
                colour=discord.Colour.orange(),
            )
        )

        return await member.kick()


async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(verification(bot))