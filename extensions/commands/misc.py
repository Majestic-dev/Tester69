import asyncio
import datetime
import json
import os
import random
import time
from typing import Optional

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

from utils import DataManager, Paginator


class misc(commands.Cog):
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
        await interaction.response.send_message(embed=embed, ephemeral=True)

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
        await interaction.response.send_message(embed=embed, ephemeral=True)

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
        await interaction.response.send_message(embed=embed, ephemeral=True)

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
        await interaction.response.send_message(embed=embed, ephemeral=True)

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
            embed=discord.Embed(description=f"🤣 {data}", colour=discord.Colour.green()),
            ephemeral=True,
        )

    @app_commands.command(
        name="wikipedia", description="Get a definition from Wikipedia"
    )
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    @app_commands.describe(
        search="The keyword you want to search the definition from Wikipedia"
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
        await Paginator.Simple().paginate(interaction, pages=embeds)

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
        await interaction.response.send_message(embed=embed, ephemeral=True)

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
                description=f"* **Last Updated:** {discord.utils.format_dt(datetime.date.fromtimestamp(data['updated'] / 1000), style='F')}\n"
                f"* **Cases:** {data['cases']}\n"
                f"* **Deaths:** {data['deaths']}\n"
                f"* **Recovered:** {data['recovered']}\n"
                f"* **Active:** {data['active']}\n"
                f"* **Critical:** {data['critical']}\n"
                f"* **Cases Today:** {data['todayCases']}\n"
                f"* **Deaths Today:** {data['todayDeaths']}\n"
                f"* **Tests:** {data['tests']}\n"
                f"* **Population:** {data['population']}",
                colour=discord.Colour.dark_red(),
            )

            embed.set_footer(
                icon_url=interaction.user.avatar,
                text=f"Requested by - {interaction.user} | Powered by NovelCOVID API ❤️",
            )
            embed.set_thumbnail(url=data["countryInfo"]["flag"])
        except KeyError:
            embed = discord.Embed(colour=discord.Colour.red())
            embed.description = "<:white_cross:1096791282023669860> Couldn't find a country with that name"
        await session.close()
        await interaction.response.send_message(embed=embed, ephemeral=True)

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
                description=f"* **Last Updated:** {discord.utils.format_dt(datetime.datetime.fromtimestamp(data['dt']), style='F')}\n"
                f"* **Sunrise:** {discord.utils.format_dt(datetime.datetime.fromtimestamp(data['sys']['sunrise']), style='T')}\n"
                f"* **Sunset:** {discord.utils.format_dt(datetime.datetime.fromtimestamp(data['sys']['sunset']), style='T')}\n"
                f"* **Description:** {data['weather'][0]['description']}\n"
                f"* **Temperature:** {round(data['main']['temp'] - 273.15)}°C\n"
                f"* **Feels Like:** {round(data['main']['feels_like'] - 273.15)}°C\n"
                f"* **Humidity:** {data['main']['humidity']}%\n"
                f"* **Wind Speed:** {int(data['wind']['speed'] * 1.60934)} km/h ({data['wind']['speed']} mph)\n"
                f"* **Cloudiness:** {data['clouds']['all']}%",
                colour=discord.Colour.blurple(),
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
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(
        name="forecast",
        description="Get the weather forecast for a location (in 3 hour intervals)",
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
                colour=discord.Colour.from_rgb(173, 216, 230),
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
                    name=f"{datetime.datetime.fromtimestamp(data['list'][i]['dt']).strftime('%H:%M')} - {datetime.datetime.fromtimestamp(data['list'][i]['dt']).strftime('%d/%m/%Y')}",
                    value=f"{data['list'][i]['weather'][0]['description']}\n{round(data['list'][i]['main']['temp'] - 273.15)}°C",
                    inline=True,
                )
        except IndexError:
            embed = discord.Embed(colour=discord.Colour.red())
            embed.description = "<:white_cross:1096791282023669860> Couldn't find a location with that name"
        await session.close()
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(
        name="count", description="Count from one number to another number"
    )
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    @app_commands.describe(
        start="The number you want to start counting from",
        end="The number you want to stop counting at",
    )
    async def count(
        self,
        interaction: discord.Interaction,
        start: int,
        end: int,
    ):
        await interaction.response.defer(ephemeral=True)
        while start <= end:
            with open(f"{interaction.user.id}.txt", "a") as f:
                f.write(f"{start}\n")
                start += 1
        await interaction.followup.send(
            ephemeral=True, file=discord.File(f"{interaction.user.id}.txt")
        )
        os.remove(f"{interaction.user.id}.txt")

    @app_commands.command(
        name="transcript", description="Get a transcript of a channel"
    )
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    @app_commands.describe(channel="The channel you want to get the transcript of")
    async def transcript(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        await interaction.response.defer(ephemeral=True)
        messagelist = []

        async for message in channel.history(limit=None):
            asyncio.sleep(1)
            messagelist.append(message)

        for message in reversed(messagelist):
            with open(
                f"{channel.id}_{interaction.user.id}.txt", "a", encoding="utf-8"
            ) as f:
                if message.embeds:
                    f.write(f"\n{message.author} EMBED\n")
                    if message.embeds[0].title:
                        f.write(f"TITLE - {message.embeds[0].title}\n")
                    if message.embeds[0].description:
                        f.write(f"DESCRIPTION - {message.embeds[0].description}\n")
                    if len(message.embeds[0].fields) > 0:
                        for field in message.embeds[0].fields:
                            f.write(f"FIELD - {field.name} - {field.value}\n")
                    if message.embeds[0].footer:
                        f.write(f"FOOTER - {message.embeds[0].footer.text}\n")
                    if message.embeds[0].image:
                        f.write(f"IMAGE - {message.embeds[0].image.url}\n")
                    if message.embeds[0].thumbnail:
                        f.write(f"THUMBNAIL - {message.embeds[0].thumbnail.url}\n")
                    if message.embeds[0].author:
                        f.write(f"AUTHOR - {message.embeds[0].author.name}\n")
                    if message.embeds[0].url:
                        f.write(f"EMBED URL LINK - {message.embeds[0].url}\n")
                    f.write(f"MESSAGE LINK - {message.jump_url}\n\n")
                    continue
                if message.attachments:
                    f.write(f"\n{message.author} ATTACHMENT\n")
                    f.write(f"ATTACHMENT URL - {message.attachments[0].url}\n")
                    f.write(f"MESSAGE LINK - {message.jump_url}\n\n")
                    continue
                f.write(f"{message.author} - {message.content} - {message.jump_url}\n")
        await interaction.followup.send(
            file=discord.File(f"{channel.id}.txt"), ephemeral=True
        )
        os.remove(f"{channel.id}_{interaction.user.id}.txt")

    @app_commands.command(
        name="report", description="Report a bug or issue with the bot"
    )
    @app_commands.choices(
        choices=[
            app_commands.Choice(name="Report a bug", value="bug"),
            app_commands.Choice(name="Report a suggestion", value="suggestion"),
            app_commands.Choice(name="Report a spelling error", value="typo"),
            app_commands.Choice(name="Report abuse", value="abuse"),
            app_commands.Choice(name="Report something else", value="other"),
        ]
    )
    async def report(
        self,
        interaction: discord.Interaction,
        choices: app_commands.Choice[str],
        description: str,
    ):
        user_data = await DataManager.get_user_data(interaction.user.id)
        cooldowns = user_data["cooldowns"]

        if len(description) < 100:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> Your report description can't be shorter than 100 characters, please try to be more descriptive",
                    colour=discord.Colour.red(),
                ),
                ephemeral=True,
            )

        if choices.value == "bug":
            choices = "Bug Report"
        elif choices.value == "suggestion":
            choices = "Suggestion"
        elif choices.value == "typo":
            choices = "Spelling Error Report"
        elif choices.value == "abuse":
            choices = "Abuse Report"
        elif choices.value == "other":
            choices = "Other Report"

        if cooldowns is None or "report" not in cooldowns:
            await DataManager.add_cooldown(interaction.user.id, "report", 86400)

        elif "report" in cooldowns:
            startTime = datetime.datetime.strptime(
                cooldowns["report"], "%Y-%m-%dT%H:%M:%S.%f"
            )
            endTime = datetime.datetime.strptime(
                discord.utils.utcnow().isoformat(), "%Y-%m-%dT%H:%M:%S.%f"
            )
            timeLeft = (startTime - endTime).total_seconds()

            if json.loads(cooldowns)["report"] < discord.utils.utcnow().isoformat():
                await DataManager.remove_cooldown(interaction.user.id, "report")
                await DataManager.add_cooldown(interaction.user.id, "report", 86400)

            if json.loads(cooldowns)["report"] > discord.utils.utcnow().isoformat():
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        description=f"<:white_cross:1096791282023669860> You already sent a report in the last 24 hours, try again <t:{int(time.time() + timeLeft)}:R>",
                        colour=discord.Colour.red(),
                    ),
                    ephemeral=True,
                )

        await self.bot.get_user(self.bot.owner_id).send(
            embed=discord.Embed(
                title=f"New {choices} report from {interaction.user}",
                description=description,
                colour=discord.Colour.green(),
            )
        )

        return await interaction.response.send_message(
            embed=discord.Embed(
                description=f"<:white_checkmark:1096793014287995061> Your {choices} report has been sent to the bot owner, thank you for your feedback!",
                colour=discord.Colour.green(),
            ),
            ephemeral=True,
        )


async def setup(bot):
    await bot.add_cog(misc(bot))
