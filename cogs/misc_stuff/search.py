import json
import random

from typing import Optional

import aiohttp
import discord
from discord.ext import commands

from discord import app_commands

from utils import DataManager, Paginator

class search(commands.GroupCog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(
        name="giphy", description="Search a gif by keyword from Giphy"
    )
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    @app_commands.describe(search="The keyword you want to search the Gif by")
    async def search_gif(self, interaction: discord.Interaction, search: Optional[str]):
        embed = discord.Embed(
            title=(f"{search} Gif" if search != None else "Random Gif"),
            colour=discord.Colour.green(),
        )

        if search != None:
            search.replace(" ", "+")

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    (
                        f"https://api.giphy.com/v1/gifs/random?api_key="
                        + DataManager.get("config", "giphy_key")
                    )
                    if search is None
                    else (
                        f"http://api.giphy.com/v1/gifs/search?q={search}&api_key="
                        + DataManager.get("config", "giphy_key")
                    )
                ) as response:
                    data = json.loads(await response.text())
                    gif_choice = random.randint(0, 9)
                    embed.set_image(
                        url=data["data"][gif_choice]["images"]["original"]["url"]
                    )
            except IndexError:
                response = await session.get(
                    f"https://api.giphy.com/v1/gifs/random?api_key="
                    + DataManager.get("config", "giphy_key")
                )
                data = json.loads(await response.text())
                embed.set_image(url=data["data"]["images"]["original"]["url"])

        embed.set_footer(
            icon_url=interaction.user.avatar,
            text=f"Requested by - {interaction.user} | Powered by Giphy API ❤️",
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(
        name="unsplash", description="Search an image by keyword from Unsplash"
    )
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    @app_commands.describe(search="The keyword you want to search the image by")
    async def search_unsplash(
        self, interaction: discord.Interaction, search: Optional[str]
    ):
        embed = discord.Embed(
            title=(f"{search} Image" if search != None else "Random Image"),
            colour=discord.Colour.green(),
        )

        if search != None:
            search.replace(" ", "+")

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    (
                        f"https://api.unsplash.com/photos/random?client_id="
                        + DataManager.get("config", "unsplash_key")
                    )
                    if search is None
                    else (
                        f"https://api.unsplash.com/search/photos?query={search}&client_id="
                        + DataManager.get("config", "unsplash_key")
                    )
                ) as response:
                    data = json.loads(await response.text())
                    embed.set_image(url=data["urls"]["full"])

                    data = json.loads(await response.text())
                    image_choice = random.randint(0, 9)
                    embed.set_image(url=data["results"][image_choice]["urls"]["full"])
            except IndexError:
                response = await session.get(
                    f"https://api.unsplash.com/photos/random?client_id="
                    + DataManager.get("config", "unsplash_key")
                )
                data = json.loads(await response.text())
                embed.set_image(url=data["urls"]["full"])

        await session.close()
        embed.set_footer(
            icon_url=interaction.user.avatar,
            text=f"Requested by - {interaction.user} | Powered by Unsplash API ❤️",
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(
        name="wikipedia", description="Get a definition from Wikipedia"
    )
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    @app_commands.describe(
        search="The keyword you want to search the definition from Wikipedia"
    )
    async def wikipedia(self, interaction: discord.Interaction, *, search: str):
        async with aiohttp.ClientSession() as session:
            try:
                response = await session.get(
                    f"https://en.wikipedia.org/api/rest_v1/page/summary/{search}"
                )
                data = json.loads(await response.text())
                embed = discord.Embed(
                    title=f"📚 {search}", colour=discord.Colour.green()
                )
                embed.url = data["content_urls"]["desktop"]["page"]
                embed.description = data["extract"]
                embed.set_footer(
                    icon_url=interaction.user.avatar,
                    text=f"Requested by - {interaction.user} | Powered by Wikipedia API ❤️",
                )
                try:
                    embed.set_thumbnail(url=data["thumbnail"]["source"])
                except KeyError:
                    pass
            except:
                embed = discord.Embed(
                    description="<:white_cross:1096791282023669860> Couldn't find a Wikipedia article with that name",
                    colour=discord.Colour.red(),
                )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(
        name="urban", description="Get a definition from Urban Dictionary"
    )
    @app_commands.describe(
        search="The keyword you want to search the definition from The Urban Dictionary"
    )
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    async def urban(self, interaction: discord.Interaction, *, search: str = None):
        embeds = []

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.urbandictionary.com/v0/random"
                if search is None
                else f"https://api.urbandictionary.com/v0/define?term={search}"
            ) as response:
                for word in json.loads(await response.text())["list"]:
                    try:
                        embed = discord.Embed(
                            title=f"📚 {word['word']}", colour=discord.Colour.green()
                        )
                        embed.url = word["permalink"]
                        embed.description = (
                            word["definition"].replace("[", "").replace("]", "")
                        )
                        embed.set_footer(
                            icon_url=interaction.user.avatar,
                            text=f"Requested by - {interaction.user} | Powered by Urban Dictionary API ❤️",
                        )
                        embeds.append(embed)
                    except IndexError:
                        embed = discord.Embed(
                            description="<:white_cross:1096791282023669860> Couldn't find a definition for that term",
                            colour=discord.Colour.red(),
                        )

        await Paginator.Simple().paginate(interaction, pages=embeds)

    @app_commands.command(name="github", description="Get a user's GitHub profile")
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    @app_commands.describe(
        search="The GitHub username you want to search the profile of"
    )
    async def github(self, interaction: discord.Interaction, *, search: str):
        async with aiohttp.ClientSession() as session:
            try:
                response = await session.get(f"https://api.github.com/users/{search}")
                data = json.loads(await response.text())
                embed = discord.Embed(
                    title=f"📚 {search}", colour=discord.Colour.green()
                )
                embed.url = data["html_url"]
                if data["bio"] is not None:
                    embed.description = data["bio"]
                embed.set_footer(
                    icon_url=interaction.user.avatar,
                    text=f"Requested by - {interaction.user} | Powered by GitHub API ❤️",
                )
                embed.set_thumbnail(url=data["avatar_url"])
                embed.add_field(name="Followers", value=data["followers"], inline=True)
                embed.add_field(name="Following", value=data["following"], inline=True)
                embed.add_field(
                    name="Public Repos", value=data["public_repos"], inline=True
                )
            except KeyError:
                embed = discord.Embed(colour=discord.Colour.red())
                embed.description = "<:white_cross:1096791282023669860> Couldn't find a GitHub user with that name"

        await interaction.response.send_message(embed=embed, ephemeral=True)