from . import data_manager, cooldown_error, UserData
import datetime
import json
import discord


async def cooldown_check(
    user_id, cooldown_message: str, command: str, cooldown_time: int
):
    user_data: UserData = await data_manager.get_user_data(user_id)
    cooldowns = user_data["cooldowns"]

    if cooldowns is None or command not in cooldowns:
        await data_manager.add_cooldown(user_id, command, cooldown_time)
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
            await data_manager.remove_cooldown(user_id, command)
            await data_manager.add_cooldown(user_id, command, cooldown_time)
            return True

async def is_owner(
    interaction: discord.Interaction
):
    return interaction.user.id == 705435835306213418