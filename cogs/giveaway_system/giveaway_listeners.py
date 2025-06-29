import datetime

import discord
from discord.ext import commands

from utils import data_manager

class giveaway_listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Giveaway Join Listener
    @commands.Cog.listener()
    async def on_giveaway_join(self, giveaway_id: int):
        giveaway_data = await data_manager.get_giveaway_data(giveaway_id)
        channel = self.bot.get_channel(giveaway_data["channel_id"])
        message = await channel.fetch_message(giveaway_id)
        end_date = datetime.datetime.strptime(
            giveaway_data["end_date"], "%Y-%m-%dT%H:%M:%S.%f%z"
        )

        if message:
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
        else:
            return

    # Giveaway Leave Listener
    @commands.Cog.listener()
    async def on_giveaway_leave(self, giveaway_id: int):
        giveaway_data = await data_manager.get_giveaway_data(giveaway_id)
        channel = self.bot.get_channel(giveaway_data["channel_id"])
        message = await channel.fetch_message(giveaway_id)
        end_date = datetime.datetime.strptime(
            giveaway_data["end_date"], "%Y-%m-%dT%H:%M:%S.%f%z"
        )

        if message:
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
        else:
            return

    # Manual Giveaway End Listener
    @commands.Cog.listener()
    async def on_manual_giveaway_end(self, giveaway_id: int):
        giveaway_data = await data_manager.get_giveaway_data(giveaway_id)
        channel = self.bot.get_channel(giveaway_data["channel_id"])
        message = await channel.fetch_message(giveaway_id)
        winners = await data_manager.draw_giveaway_winners(giveaway_id)
        end_date = datetime.datetime.strptime(
            giveaway_data["end_date"], "%Y-%m-%dT%H:%M:%S.%f%z"
        )

        if message:
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
                ).set_footer(
                    text=f'"/giveaway reroll {giveaway_id}" to reroll the giveaway winners'
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
        else:
            return

    # Manual Giveaway Reroll Listener
    @commands.Cog.listener()
    async def on_manual_giveaway_reroll(self, giveaway_id: int):
        giveaway_data = await data_manager.get_giveaway_data(giveaway_id)
        channel = self.bot.get_channel(giveaway_data["channel_id"])
        message = await channel.fetch_message(giveaway_id)
        winners = await data_manager.draw_giveaway_winners(giveaway_id)
        end_date = datetime.datetime.strptime(
            giveaway_data["end_date"], "%Y-%m-%dT%H:%M:%S.%f%z"
        )

        if message:
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
        else:
            return

    # Manual Giveaway Winner Reroll Listener
    @commands.Cog.listener()
    async def on_manual_giveaway_winner_reroll(
        self, giveaway_id: int, new_winner_id: int
    ):
        giveaway_data = await data_manager.get_giveaway_data(giveaway_id)
        channel = self.bot.get_channel(giveaway_data["channel_id"])
        message = await channel.fetch_message(giveaway_id)
        end_date = datetime.datetime.strptime(
            giveaway_data["end_date"], "%Y-%m-%dT%H:%M:%S.%f%z"
        )

        if message:
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
        else:
            return
        
async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(giveaway_listeners(bot))