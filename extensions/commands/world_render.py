import os

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from PIL import Image, ImageDraw, UnidentifiedImageError


class world_render(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    async def load_render(self, world: str, member_id: int):
            session = aiohttp.ClientSession()
            response = await session.get(
                f"http://world.growtopiagame.com/{world}.png"
            )
            data = await response.read()
            await session.close()
            with open(f"{member_id}.png", "wb") as f:
                f.write(data)
            image = Image.open(f"{member_id}.png")
            draw = ImageDraw.Draw(image)
            return image, draw

    @app_commands.command(name="gt_world", description="Get a world render from growtopia (if the world is rendered)")
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    async def world_gt(self, interaction: discord.Interaction, world: str):
        print("smash")
        await interaction.response.defer()
        embed = discord.Embed(colour=discord.Colour.green())
        try:
            await self.load_render(world, interaction.user.id)
        except UnidentifiedImageError:
            os.remove(f"{interaction.user.id}.png")
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description=f"<:white_cross:1096791282023669860> That world does not seem to be rendered. If you own that world, do `/renderworld` in-game!",
                    colour=discord.Colour.red(),
                    )
                )
        embed.add_field(name="", value=f"**World | [{world.upper()}](http://world.growtopiagame.com/{world}.png)**", inline=False)
        embed.set_image (url=f"attachment://{interaction.user.id}.png")
        embed.set_footer(
            icon_url=interaction.user.avatar, text=f"Requested by - {interaction.user}"
        )
        await interaction.edit_original_response(embed=embed, attachments=[discord.File(f"{interaction.user.id}.png")])
        os.remove(f"{interaction.user.id}.png")

async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(world_render(bot))