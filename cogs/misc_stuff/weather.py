import datetime
import json

import aiohttp
import discord
from discord.ext import commands

from discord import app_commands

from utils import data_manager

class weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="weather", description="Get the weather for a location")
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    @app_commands.describe(search="The location you want to search the weather for")
    async def weather(self, interaction: discord.Interaction, *, search: str):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    f"http://api.openweathermap.org/geo/1.0/direct?q={search}&limit=1&appid="
                    + data_manager.get("config", "weather_api_key")
                ) as location:
                    lat = json.loads(await location.text())[0]["lat"]
                    lon = json.loads(await location.text())[0]["lon"]

                async with session.get(
                    f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid="
                    + data_manager.get("config", "weather_api_key")
                ) as response:
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
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    f"http://api.openweathermap.org/geo/1.0/direct?q={search}&limit=1&appid="
                    + data_manager.get("config", "weather_api_key")
                ) as location:
                    lat = json.loads(await location.text())[0]["lat"]
                    lon = json.loads(await location.text())[0]["lon"]

                async with session.get(
                    f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid="
                    + data_manager.get("config", "weather_api_key")
                ) as response:
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

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(weather(bot))