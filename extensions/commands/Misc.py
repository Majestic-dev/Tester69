import json
import random
from datetime import datetime
from typing import Optional

import aiohttp
import discord
import Paginator
from discord import app_commands
from discord.ext import commands

from utils import DataManager


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="search_giphy", description="Search a gif by keyword from Giphy"
    )
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    @app_commands.describe(search="The keyword you want to search the Gif by")
    async def search_gif(self, interaction: discord.Interaction, search: Optional[str]):
        if search == None:
            search1 = "Random Gif"
        else:
            search1 = search + " Gif"
        embed = discord.Embed(title=f"{search1}", colour=discord.Colour.green())
        session = aiohttp.ClientSession()
        try:
            if search == None:
                response = await session.get(
                    f"https://api.giphy.com/v1/gifs/random?api_key="
                    + DataManager.get("config", "giphy_key")
                )
                data = json.loads(await response.text())
                embed.set_image(url=data["data"]["images"]["original"]["url"])
            else:
                search.replace(" ", "+")
                response = await session.get(
                    f"http://api.giphy.com/v1/gifs/search?q={search}&api_key="
                    + DataManager.get("config", "giphy_key")
                )
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

        await session.close()
        embed.set_footer(
            icon_url=interaction.user.avatar,
            text=f"Requested by - {interaction.user} | Powered by Giphy API ❤️",
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="search_unsplash", description="Search an image by keyword from Unsplash"
    )
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    @app_commands.describe(search="The keyword you want to search the image by")
    async def search_unsplash(
        self, interaction: discord.Interaction, search: Optional[str]
    ):
        if search == None:
            search1 = "Random Image"
        else:
            search1 = search + " Image"
        embed = discord.Embed(title=f"{search1}", colour=discord.Colour.green())
        session = aiohttp.ClientSession()

        try:
            if search == None:
                response = await session.get(
                    f"https://api.unsplash.com/photos/random?client_id="
                    + DataManager.get("config", "unsplash_key")
                )
                data = json.loads(await response.text())
                embed.set_image(url=data["urls"]["full"])
            else:
                search.replace(" ", "+")
                response = await session.get(
                    f"https://api.unsplash.com/search/photos?query={search}&client_id="
                    + DataManager.get("config", "unsplash_key")
                )
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
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="cat", description="Get a random cat image")
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    async def cat(self, interaction: discord.Interaction):
        session = aiohttp.ClientSession()
        response = await session.get("https://api.thecatapi.com/v1/images/search")
        data = json.loads(await response.text())
        embed = discord.Embed(title="🐱 Meow", colour=discord.Colour.green())
        embed.url = data[0]["url"]
        embed.set_image(url=data[0]["url"])
        await session.close()
        embed.set_footer(
            icon_url=interaction.user.avatar,
            text=f"Requested by - {interaction.user} | Powered by The Cat API ❤️",
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="dog", description="Get a random dog image")
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    async def dog(self, interaction: discord.Interaction):
        session = aiohttp.ClientSession()
        response = await session.get("https://api.thedogapi.com/v1/images/search")
        data = json.loads(await response.text())
        embed = discord.Embed(title=f"🐶 Woof...", colour=discord.Colour.green())
        embed.url = data[0]["url"]
        embed.set_image(url=data[0]["url"])
        await session.close()
        embed.set_footer(
            icon_url=interaction.user.avatar,
            text=f"Requested by - {interaction.user} | Powered by The Dog API ❤️",
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="dadjoke", description="Get a random dad joke")
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    async def dadjoke(self, interaction: discord.Interaction):
        session = aiohttp.ClientSession()
        response = await session.get(
            "https://icanhazdadjoke.com/", headers={"Accept": "text/plain"}
        )
        data = await response.text()
        await session.close()
        await interaction.response.send_message(
            embed=discord.Embed(description=f"🤣 {data}", colour=discord.Colour.green())
        )

    @app_commands.command(
        name="wikipedia", description="Get a definition from Wikipedia"
    )
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    @app_commands.describe(
        search="The keyword you want to search the definition from Wikipedia by"
    )
    async def wikipedia(self, interaction: discord.Interaction, *, search: str):
        try:
            session = aiohttp.ClientSession()
            response = await session.get(
                f"https://en.wikipedia.org/api/rest_v1/page/summary/{search}"
            )
            data = json.loads(await response.text())
            embed = discord.Embed(title=f"📚 {search}", colour=discord.Colour.green())
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
        await session.close()
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="urban", description="Get a definition from Urban Dictionary"
    )
    @app_commands.describe(
        search="The keyword you want to search the definition from The Urban Dictionary by"
    )
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    async def urban(self, interaction: discord.Interaction, *, search: str = None):
        embeds = []

        session = aiohttp.ClientSession()

        if search is None:
            response = await session.get(f"https://api.urbandictionary.com/v0/random")
        else:
            response = await session.get(
                f"https://api.urbandictionary.com/v0/define?term={search}"
            )

        for word in json.loads(await response.text())["list"]:
            try:
                embed = discord.Embed(
                    title=f"📚 {word['word']}", colour=discord.Colour.green()
                )
                embed.url = word["permalink"]
                embed.description = word["definition"].replace("[", "").replace("]", "")
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
        await session.close()
        await Paginator.Simple().start(interaction, pages=embeds)

    @app_commands.command(name="github", description="Get a user's GitHub profile")
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    @app_commands.describe(
        search="The GitHub username you want to search the profile of"
    )
    async def github(self, interaction: discord.Interaction, *, search: str):
        session = aiohttp.ClientSession()
        try:
            response = await session.get(f"https://api.github.com/users/{search}")
            data = json.loads(await response.text())
            embed = discord.Embed(title=f"📚 {search}", colour=discord.Colour.green())
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
        await session.close()
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="covid", description="Get the COVID-19 stats for a country"
    )
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    @app_commands.describe(
        search="The country you want to search the COVID-19 stats for"
    )
    async def covid(self, interaction: discord.Interaction, *, search: str):
        session = aiohttp.ClientSession()
        try:
            response = await session.get(
                f"https://corona.lmao.ninja/v2/countries/{search}"
            )
            data = json.loads(await response.text())
            embed = discord.Embed(
                title=f"COVID-19 Statistics for {search}",
                colour=discord.Colour.from_rgb(29, 29, 29),
            )
            embed.add_field(name="Cases", value=data["cases"], inline=True)
            embed.add_field(name="Deaths", value=data["deaths"], inline=True)
            embed.add_field(name="Recovered", value=data["recovered"], inline=True)
            embed.add_field(name="Active", value=data["active"], inline=True)
            embed.add_field(name="Critical", value=data["critical"], inline=True)
            embed.add_field(name="Cases Today", value=data["todayCases"], inline=True)
            embed.add_field(name="Deaths Today", value=data["todayDeaths"], inline=True)
            embed.add_field(name="Tests", value=data["tests"], inline=True)
            embed.add_field(name="Population", value=data["population"], inline=True)
            embed.set_footer(
                icon_url=interaction.user.avatar,
                text=f"Requested by - {interaction.user} | Powered by NovelCOVID API ❤️",
            )
            embed.set_thumbnail(url=data["countryInfo"]["flag"])
        except KeyError:
            embed = discord.Embed(colour=discord.Colour.red())
            embed.description = "<:white_cross:1096791282023669860> Couldn't find a country with that name"
        await session.close()
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="weather", description="Get the weather for a location")
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    @app_commands.describe(search="The location you want to search the weather for")
    async def weather(self, interaction: discord.Interaction, *, search: str):
        session = aiohttp.ClientSession()
        try:
            location = await session.get(
                f"http://api.openweathermap.org/geo/1.0/direct?q={search}&limit=1&appid="
                + DataManager.get("config", "weather_api_key")
            )
            lat = json.loads(await location.text())[0]["lat"]
            lon = json.loads(await location.text())[0]["lon"]

            response = await session.get(
                f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid="
                + DataManager.get("config", "weather_api_key")
            )
            data = json.loads(await response.text())
            embed = discord.Embed(
                title=f"Weather for {search}",
                colour=discord.Colour.from_rgb(29, 29, 29),
            )
            embed.add_field(
                name="Description", value=data["weather"][0]["description"], inline=True
            )
            embed.add_field(
                name="Temperature",
                value=f"{round(data['main']['temp'] - 273.15)}°C",
                inline=True,
            )
            embed.add_field(
                name="Feels Like",
                value=f"{round(data['main']['feels_like'] - 273.15)}°C",
                inline=True,
            )
            embed.add_field(
                name="Humidity", value=f"{data['main']['humidity']}%", inline=True
            )
            embed.add_field(
                name="Wind Speed", value=f"{data['wind']['speed']}mph", inline=True
            )
            embed.add_field(
                name="Cloudiness", value=f"{data['clouds']['all']}%", inline=True
            )
            embed.set_footer(
                icon_url=interaction.user.avatar,
                text=f"Requested by - {interaction.user} | Powered by OpenWeatherMap API ❤️",
            )
            embed.set_thumbnail(
                url=f"http://openweathermap.org/img/w/{data['weather'][0]['icon']}.png"
            )
        except IndexError:
            embed = discord.Embed(colour=discord.Colour.red())
            embed.description = "<:white_cross:1096791282023669860> Couldn't find a location with that name"
        await session.close()
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="forecast",
        description="Get the weather forecast for a location (3 hour intervals)",
    )
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    @app_commands.describe(
        search="The location you want to search the weather forecast for"
    )
    async def forecast(self, interaction: discord.Interaction, *, search: str):
        session = aiohttp.ClientSession()
        try:
            location = await session.get(
                f"http://api.openweathermap.org/geo/1.0/direct?q={search}&limit=1&appid="
                + DataManager.get("config", "weather_api_key")
            )
            lat = json.loads(await location.text())[0]["lat"]
            lon = json.loads(await location.text())[0]["lon"]

            response = await session.get(
                f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid="
                + DataManager.get("config", "weather_api_key")
            )
            data = json.loads(await response.text())
            embed = discord.Embed(
                title=f"Weather Forecast for {search}",
                colour=discord.Colour.from_rgb(29, 29, 29),
            )
            embed.set_footer(
                icon_url=interaction.user.avatar,
                text=f"Requested by - {interaction.user} | Powered by OpenWeatherMap API ❤️",
            )
            embed.set_thumbnail(
                url=f"http://openweathermap.org/img/w/{data['list'][0]['weather'][0]['icon']}.png"
            )
            for i in range(0, 5):
                embed.add_field(
                    name=f"{datetime.fromtimestamp(data['list'][i]['dt']).strftime('%H:%M')} - {datetime.fromtimestamp(data['list'][i]['dt']).strftime('%d/%m/%Y')}",
                    value=f"{data['list'][i]['weather'][0]['description']}\n{round(data['list'][i]['main']['temp'] - 273.15)}°C",
                    inline=True,
                )
        except IndexError:
            embed = discord.Embed(colour=discord.Colour.red())
            embed.description = "<:white_cross:1096791282023669860> Couldn't find a location with that name"
        await session.close()
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Misc(bot))
