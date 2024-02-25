import json

import discord
from discord.ext import commands, tasks

from utils import DataManager

class cooldown_looper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_listener(self.on_ready)

    async def on_ready(self):
        self.cooldown_loop.start()
        

    @tasks.loop(seconds=5)
    async def cooldown_loop(self):
        all_users = await DataManager.get_all_users()
        for user in all_users:
            user_data = await DataManager.get_user_data(user)
            if user_data["cooldowns"] is not None:
                cooldowns = json.loads(user_data["cooldowns"])
                for command in cooldowns:
                    if cooldowns[command] < discord.utils.utcnow().isoformat():
                        await DataManager.remove_cooldown(user, command)

async def setup(bot):
    await bot.add_cog(cooldown_looper(bot))