import datetime

import discord
from discord.ext import commands, tasks

from utils import DataManager


class giveaway_looper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.giveawayloop.start()

    @tasks.loop(seconds=10)
    async def giveawayloop(self):
        async with DataManager.db_connection.acquire():
            ended_giveaways = await DataManager.db_connection.fetch(
                "SELECT * FROM giveaways WHERE end_date < $1 AND ended = FALSE",
                discord.utils.utcnow().isoformat(),
            )
            ended_giveaways = [dict(giveaway) for giveaway in ended_giveaways]

            for giveaway in ended_giveaways:
                await DataManager.end_giveaway(giveaway["id"], giveaway["guild_id"])
                channel = self.bot.get_channel(giveaway["channel_id"])
                try:
                    message = await channel.fetch_message(giveaway["id"])
                except discord.NotFound:
                    return
                winners = await DataManager.draw_giveaway_winners(
                    giveaway["id"], giveaway["guild_id"]
                )
                end_date = datetime.datetime.strptime(
                    giveaway["end_date"], "%Y-%m-%dT%H:%M:%S.%f%z"
                )

                if winners is False:
                    try:
                        await message.edit(
                            view=None,
                        )
                        return await message.reply(
                            f"Unfortunately, nobody entered the giveaway for the **{giveaway['prize']}**"
                        )
                    except:
                        return

                try:
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
                            text=f"`/giveaway reroll {giveaway['id']}` to reroll the giveaway winners",
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
                except:
                    return

        next_giveaway = await DataManager.get_next_giveaway()

        if next_giveaway is None:
            pass
        else:
            end_date = datetime.datetime.fromisoformat(next_giveaway["end_date"])
            await discord.utils.sleep_until(end_date)
            channel = self.bot.get_channel(next_giveaway["channel_id"])
            message = await channel.fetch_message(next_giveaway["id"])
            await DataManager.end_giveaway(
                next_giveaway["id"], next_giveaway["guild_id"]
            )
            winners = await DataManager.draw_giveaway_winners(
                next_giveaway["id"], next_giveaway["guild_id"]
            )
            end_date = datetime.datetime.strptime(
                next_giveaway["end_date"], "%Y-%m-%dT%H:%M:%S.%f%z"
            )

            if winners is False:
                try:
                    await message.edit(
                        view=None,
                    )
                    return await message.reply(
                        f"Unfortunately, nobody entered the giveaway for the **{next_giveaway['prize']}**"
                    )
                except:
                    return

            try:
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
                        text=f"`/giveaway reroll {next_giveaway['id']}` to reroll the giveaway winners"
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
            except:
                return

    # Giveaway Join Listener
    @commands.Cog.listener()
    async def on_giveaway_join(self, giveaway_id: int, guild_id: int):
        giveaway_data = await DataManager.get_giveaway_data(giveaway_id, guild_id)
        channel = self.bot.get_channel(giveaway_data["channel_id"])
        message = await channel.fetch_message(giveaway_id)
        end_date = datetime.datetime.strptime(
            giveaway_data["end_date"], "%Y-%m-%dT%H:%M:%S.%f%z"
        )

        try:
            await message.edit(
                embed=discord.Embed(
                    title=f"{giveaway_data['prize']}",
                    description=(
                        f"{giveaway_data['extra_notes']}\n\n"
                        if giveaway_data["extra_notes"] is not None
                        else ""
                    )
                    + f"Ends: {discord.utils.format_dt(end_date, style='R')} ({discord.utils.format_dt(end_date, style='F')})\n"
                    f"Hosted by: <@{giveaway_data['host_id']}>\n"
                    f"Entries: **{len(giveaway_data['participants'])}**\n"
                    f"Winners: **{giveaway_data['winner_amount']}**",
                )
            )
        except Exception as e:
            print(e)
            return

    # Giveaway Leave Listener
    @commands.Cog.listener()
    async def on_giveaway_leave(self, giveaway_id: int, guild_id: int):
        giveaway_data = await DataManager.get_giveaway_data(giveaway_id, guild_id)
        channel = self.bot.get_channel(giveaway_data["channel_id"])
        message = await channel.fetch_message(giveaway_id)
        end_date = datetime.datetime.strptime(
            giveaway_data["end_date"], "%Y-%m-%dT%H:%M:%S.%f%z"
        )

        try:
            await message.edit(
                embed=discord.Embed(
                    title=f"{giveaway_data['prize']}",
                    description=(
                        f"{giveaway_data['extra_notes']}\n\n"
                        if giveaway_data["extra_notes"] is not None
                        else ""
                    )
                    + f"Ends: {discord.utils.format_dt(end_date, style='R')} ({discord.utils.format_dt(end_date, style='F')})\n"
                    f"Hosted by: <@{giveaway_data['host_id']}>\n"
                    f"Entries: **{len(giveaway_data['participants'])}**\n"
                    f"Winners: **{giveaway_data['winner_amount']}**",
                )
            )
        except:
            return

    # Manual Giveaway End Listener
    @commands.Cog.listener()
    async def on_manual_giveaway_end(self, giveaway_id: int, guild_id: int):
        giveaway_data = await DataManager.get_giveaway_data(giveaway_id, guild_id)
        channel = self.bot.get_channel(giveaway_data["channel_id"])
        message = await channel.fetch_message(giveaway_id)
        winners = await DataManager.draw_giveaway_winners(giveaway_id, guild_id)
        end_date = datetime.datetime.strptime(
            giveaway_data["end_date"], "%Y-%m-%dT%H:%M:%S.%f%z"
        )

        try:
            await message.edit(
                embed=discord.Embed(
                    title=f"{giveaway_data['prize']}",
                    description=(
                        f"{giveaway_data['extra_notes']}\n\n"
                        if giveaway_data["extra_notes"] is not None
                        else ""
                    )
                    + f"Ended: {discord.utils.format_dt(end_date, style='R')} ({discord.utils.format_dt(end_date, style='F')})\n"
                    f"Hosted by: <@{giveaway_data['host_id']}>\n"
                    f"Entries: **{len(giveaway_data['participants'])}**\n"
                    + (
                        f"Winners: {','.join([f'<@{winner}>' for winner in winners])}"
                        if len(winners) > 0
                        else "Winners: No Winners"
                    ),
                ),
                view=None,
            )
            if len(winners) > 0:
                await message.reply(
                    f"Congratulations {', '.join([f'<@{winner}>' for winner in winners])}! You have won the **{giveaway_data['prize']}**"
                )
            else:
                await message.reply(
                    f"Unfortunately, nobody entered the giveaway for the **{giveaway_data['prize']}**"
                )
        except Exception as e:
            print(e)
            return

    # Manual Giveaway Reroll Listener
    @commands.Cog.listener()
    async def on_manual_giveaway_reroll(self, giveaway_id: int, guild_id: int):
        giveaway_data = await DataManager.get_giveaway_data(giveaway_id, guild_id)
        channel = self.bot.get_channel(giveaway_data["channel_id"])
        message = await channel.fetch_message(giveaway_id)
        winners = await DataManager.draw_giveaway_winners(giveaway_id, guild_id)
        end_date = datetime.datetime.strptime(
            giveaway_data["end_date"], "%Y-%m-%dT%H:%M:%S.%f%z"
        )

        try:
            await message.edit(
                embed=discord.Embed(
                    title=f"{giveaway_data['prize']}",
                    description=(
                        f"{giveaway_data['extra_notes']}\n\n"
                        if giveaway_data["extra_notes"] is not None
                        else ""
                    )
                    + f"Ended: {discord.utils.format_dt(end_date, style='R')} ({discord.utils.format_dt(end_date, style='F')})\n"
                    f"Hosted by: <@{giveaway_data['host_id']}>\n"
                    f"Entries: **{len(giveaway_data['participants'])}**\n"
                    + (
                        f"Winners: {','.join([f'<@{winner}>' for winner in winners])}"
                        if len(winners) > 0
                        else "Winners: No Winners"
                    ),
                )
            )

            if len(winners) > 0:
                await message.reply(
                    f"Congratulations {', '.join([f'<@{winner}>' for winner in winners])}! You have won the **{giveaway_data['prize']}**"
                )
            else:
                await message.reply(
                    f"Unfortunately, nobody entered the giveaway for the **{giveaway_data['prize']}**"
                )
        except:
            return

    # Manual Giveaway Winner Reroll Listener
    @commands.Cog.listener()
    async def on_manual_giveaway_winner_reroll(
        self, giveaway_id: int, guild_id: int, new_winner_id: int
    ):
        giveaway_data = await DataManager.get_giveaway_data(giveaway_id, guild_id)
        channel = self.bot.get_channel(giveaway_data["channel_id"])
        message = await channel.fetch_message(giveaway_id)
        end_date = datetime.datetime.strptime(
            giveaway_data["end_date"], "%Y-%m-%dT%H:%M:%S.%f%z"
        )

        try:
            await message.edit(
                embed=discord.Embed(
                    title=f"{giveaway_data['prize']}",
                    description=(
                        f"{giveaway_data['extra_notes']}\n\n"
                        if giveaway_data["extra_notes"] is not None
                        else ""
                    )
                    + f"Ended: {discord.utils.format_dt(end_date, style='R')} ({discord.utils.format_dt(end_date, style='F')})\n"
                    f"Hosted by: <@{giveaway_data['host_id']}>\n"
                    f"Entries: {len(giveaway_data['participants'])}\n"
                    f"Winners: {','.join([f'<@{winner}>' for winner in giveaway_data['winners']])}",
                )
            )

            await message.reply(
                f"Congratulations <@{new_winner_id}>! You have won the **{giveaway_data['prize']}**"
            )
        except:
            return


async def setup(bot):
    await bot.add_cog(giveaway_looper(bot))
