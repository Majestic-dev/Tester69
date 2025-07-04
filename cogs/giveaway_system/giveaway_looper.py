import datetime

import discord
from discord.ext import commands, tasks

from utils import data_manager

class giveaway_looper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.giveawayloop.start()

    @tasks.loop(minutes=1)
    async def giveawayloop(self):
        async with data_manager.db_connection.acquire():
            ended_giveaways = await data_manager.db_connection.fetch(
                "SELECT * FROM giveaways WHERE end_date < $1 AND ended = FALSE",
                discord.utils.utcnow().isoformat(),
            )
            ended_giveaways = [dict(giveaway) for giveaway in ended_giveaways]

            for giveaway in ended_giveaways:
                await data_manager.edit_giveaway_data(giveaway["id"], "ended", True)
                channel = self.bot.get_channel(giveaway["channel_id"])
                if channel is not None:
                    try:
                        message = await channel.fetch_message(giveaway["id"])
                    except discord.errors.NotFound:
                        return
                else:
                    return
                try:
                    winners = await data_manager.draw_giveaway_winners(giveaway["id"])
                except ValueError:
                    await message.edit(
                        view=None,
                    )
                    return await message.reply(
                        f"Unfortunately, not enough people entered the giveaway for the **{giveaway['prize']}**"
                    )

                end_date = datetime.datetime.strptime(
                    giveaway["end_date"], "%Y-%m-%dT%H:%M:%S.%f%z"
                )

                if message:
                    await message.edit(
                        view=None,
                        embed=discord.Embed(
                            title=f"{giveaway['prize']}",
                            description=(
                                f"{giveaway['extra_notes']}\n\n"
                                if giveaway["extra_notes"] is not None
                                else ""
                            )
                            + f"Ended: {discord.utils.format_dt(end_date, style='R')} ({discord.utils.format_dt(end_date, style='F')})\n"
                            f"Hosted by: <@{giveaway['host_id']}>\n"
                            f"Entries: {len(giveaway['participants'])}\n"
                            + (
                                f"Winners: {','.join([f'<@{winner}>' for winner in winners])}"
                                if len(winners) > 0
                                else "Winners: No Winners"
                            ),
                        ).set_footer(
                            text=f'"/giveaway reroll {giveaway['id']}" to reroll the giveaway winners',
                        ),
                    )
                    if len(winners) > 0:
                        return await message.reply(
                            f"Congratulations {', '.join([f'<@{winner}>' for winner in winners])}! You have won the **{giveaway['prize']}**"
                        )
                    else:
                        return await message.reply(
                            f"Unfortunately, nobody entered the giveaway for the **{giveaway['prize']}**"
                        )
                else:
                    return

        next_giveaway = await data_manager.db_connection.fetchrow(
            "SELECT * FROM giveaways WHERE end_date > $1 AND ended = FALSE ORDER BY end_date ASC LIMIT 1",
            discord.utils.utcnow().isoformat(),
        )

        if next_giveaway is None:
            pass
        elif discord.utils.utcnow().isoformat() >= next_giveaway["end_date"]:
            channel = self.bot.get_channel(next_giveaway["channel_id"])
            message = await channel.fetch_message(next_giveaway["id"])
            await data_manager.edit_giveaway_data(next_giveaway["id"], "ended", True)
            winners = await data_manager.draw_giveaway_winners(next_giveaway["id"])
            end_date = datetime.datetime.strptime(
                next_giveaway["end_date"], "%Y-%m-%dT%H:%M:%S.%f%z"
            )

            if winners is False:
                if message:
                    await message.edit(
                        view=None,
                    )
                    return await message.reply(
                        f"Unfortunately, nobody entered the giveaway for the **{next_giveaway['prize']}**"
                    )
                else:
                    return

            if message:
                await message.edit(
                    view=None,
                    embed=discord.Embed(
                        title=f"{next_giveaway['prize']}",
                        description=(
                            f"{next_giveaway['extra_notes']}\n\n"
                            if next_giveaway["extra_notes"] is not None
                            else ""
                        )
                        + f"Ended: {discord.utils.format_dt(end_date, style='R')} ({discord.utils.format_dt(end_date, style='F')})\n"
                        f"Hosted by: <@{next_giveaway['host_id']}>\n"
                        f"Entries: {len(next_giveaway['participants'])}\n"
                        + (
                            f"Winners: {','.join([f'<@{winner}>' for winner in winners])}"
                            if len(winners) > 0
                            else "Winners: No Winners"
                        ),
                    ).set_footer(
                        text=f'"/giveaway reroll {next_giveaway['id']}" to reroll the giveaway winners'
                    ),
                )
                if len(winners) > 0:
                    return await message.reply(
                        f"Congratulations {', '.join([f'<@{winner}>' for winner in winners])}! You have won the **{next_giveaway['prize']}**"
                    )
                else:
                    return await message.reply(
                        f"Unfortunately, nobody entered the giveaway for the **{next_giveaway['prize']}**"
                    )
            else:
                return
        else:
            return

async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(giveaway_looper(bot))