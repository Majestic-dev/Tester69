from . import DataManager, cooldown_error
import datetime
import json
import discord

async def cooldown_check(user_id, cooldown_message: str, command: str, cooldown_time: int):
    user_data = await DataManager.get_user_data(user_id)
    cooldowns = user_data["cooldowns"]

    if cooldowns is None or command not in cooldowns:
        await DataManager.add_cooldown(user_id, command, cooldown_time)
        return True

    elif command in cooldowns:
        startTime = datetime.datetime.strptime(
            json.loads(cooldowns)[command], "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        endTime = datetime.datetime.strptime(
            discord.utils.utcnow().isoformat(), "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        timeLeft = (startTime - endTime).total_seconds()

        if json.loads(cooldowns)[command] > discord.utils.utcnow().isoformat():
            raise cooldown_error(cooldown_message, timeLeft)
        
        if json.loads(cooldowns)[command] < discord.utils.utcnow().isoformat():
            await DataManager.remove_cooldown(user_id, command)
            await DataManager.add_cooldown(user_id, command, cooldown_time)
            return True