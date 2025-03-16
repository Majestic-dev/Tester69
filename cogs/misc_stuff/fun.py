import json
import aiohttp
import discord

from discord import app_commands
from discord.ext import commands


class fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="cat", description="Get a random cat image")
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    async def cat(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.thecatapi.com/v1/images/search"
            ) as response:
                data = json.loads(await response.text())
                embed = discord.Embed(title="🐱 Meow", colour=discord.Colour.green())
                embed.url = data[0]["url"]
                embed.set_image(url=data[0]["url"])

        embed.set_footer(
            icon_url=interaction.user.avatar,
            text=f"Requested by - {interaction.user} | Powered by The Cat API ❤️",
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="dog", description="Get a random dog image")
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    async def dog(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.thedogapi.com/v1/images/search"
            ) as response:
                data = json.loads(await response.text())
                embed = discord.Embed(title="🐶 Woof", colour=discord.Colour.green())
                embed.url = data[0]["url"]
                embed.set_image(url=data[0]["url"])

        embed.set_footer(
            icon_url=interaction.user.avatar,
            text=f"Requested by - {interaction.user} | Powered by The Dog API ❤️",
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="dadjoke", description="Get a random dad joke")
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    async def dadjoke(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://icanhazdadjoke.com/", headers={"Accept": "text/plain"}
            ) as response:
                data = await response.text()

        await interaction.response.send_message(
            embed=discord.Embed(
                description=f"🤣 {data}", colour=discord.Colour.green()
            ),
            ephemeral=True,
        )