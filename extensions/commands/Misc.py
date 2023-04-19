import json
import random
from datetime import datetime
import aiohttp

import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="search_gif", description="Search a gif by keyword from Giphy")
    async def search_gif(self, interaction: discord.Interaction, search: Optional[str]):
        if search == None:
            search1 = "Random Gif"
        else:
            search1 = search + " Gif"
        embed = discord.Embed(
            title=f"{search1}",
            colour=discord.Colour.green()
        )
        session = aiohttp.ClientSession()

        if search == None:
            response = await session.get("https://api.giphy.com/v1/gifs/random?api_key=bAoZ2Hc2akTjTlm5Gcbh2l8qWNjc9QSw")
            data = json.loads(await response.text())
            embed.set_image(url=data['data']['images']['original']['url'])
        else:
            search.replace(' ', '+')
            response = await session.get(f"http://api.giphy.com/v1/gifs/search?q={search}&api_key=bAoZ2Hc2akTjTlm5Gcbh2l8qWNjc9QSw")
            data = json.loads(await response.text())
            gif_choice = random.randint(0, 9)
            embed.set_image(url=data['data'][gif_choice]['images']['original']['url'])

        await session.close()
        embed.set_footer(text=f"Requested by {interaction.user} | Powered by Giphy API ❤️")
        embed.timestamp = datetime.utcnow()
        await interaction.response.send_message(embed=embed)
            

async def setup(bot):
    await bot.add_cog(Misc(bot))
