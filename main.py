import asyncio
import logging
import os
import traceback
import time
import discord

from discord import app_commands
from discord.ext import commands

from typing import Tuple

from utils import DataManager

from cogs.giveaway_system.giveaway_commands import GiveawayViews
from cogs.ticket_system.ticket_system import (
    closed_ticket_views,
    panel_views,
    ticket_views
)

initial_extensions: Tuple[str, ...] = (
    "cogs.giveaway_system",
    "cogs.logging_system",
    "cogs.misc_stuff",
    "cogs.moderation",
    "cogs.owner_only",
    "cogs.server_info",
    "cogs.server_management",
    "cogs.ticket_system",
    "cogs.verification_system"
)

class Bot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.all()
        super().__init__(
            command_prefix="'",
            owner_id=705435835306213418,
            intents=intents
        )

    async def setup_hook(self) -> None:
        for folder in os.listdir("cogs"):
            extension_name = f"cogs.{folder}"
            if extension_name in bot.extensions:
                await bot.unload_extension(extension_name)
            try:
                    await bot.load_extension(extension_name)
            except Exception as e:
                print(f"Failed to load {extension_name}: {e}")
                await bot.reload_extension(extension_name)
        await bot.tree.sync()

        self.add_view(GiveawayViews(bot))
        self.add_view(panel_views(bot))
        tickets = await DataManager.get_all_tickets()
        panels = await DataManager.get_all_panels()

        try:
            for panel in panels:
                for ticket in tickets:
                    self.add_view(
                        view=closed_ticket_views(
                            bot,
                            panel["id"],
                            ticket["ticket_creator"],
                            ticket["ticket_id"],
                        )
                    )
                    self.add_view(
                        view=ticket_views(bot, panel["id"], ticket["ticket_creator"])
                    )
        except Exception as e:
            print(e)

bot = Bot()
handler = logging.FileHandler(
    filename="data/discord.log",
    encoding="utf-8",
    mode="w"
)

@bot.event
async def on_ready() -> None:
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game("https://discord.gg/VsDDf8YKBV")
    )

@bot.tree.error
async def on_app_command_error(
    interaction: discord.Interaction, error: app_commands.AppCommandError
):
    await interaction.response.defer(ephemeral=True)

    if isinstance(error, app_commands.errors.MissingPermissions):
        return await interaction.edit_original_response(
            embed=discord.Embed(
                description="<:white_cross:1096791282023669860> You are missing the required permissions to use this command.",
                colour=discord.Colour.red(),
            ),
        )

    elif isinstance(error, app_commands.CommandOnCooldown):
        await interaction.edit_original_response(
            embed=discord.Embed(
                description=f"<:white_cross:1096791282023669860> You can use this command again <t:{int(time.time() + error.retry_after)}:R>",
                colour=discord.Colour.red(),
            ),
        )
        await asyncio.sleep(error.retry_after)
        try:
            return await interaction.delete_original_response()
        except:
            pass


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.CommandNotFound):
        return

    if isinstance(error, commands.NotOwner):
        return

    else:
        return await bot.get_user(bot.owner_id).send(
            embed=discord.Embed(
                description=f"```py\n{traceback.format_exc()}\n```",
                colour=discord.Colour.red(),
            )
        )

async def main():
    await DataManager.initialise()
    
    discord.utils.setup_logging(handler=handler, level=logging.INFO)
    await bot.start(DataManager.get("config", "token"))

if __name__ == "__main__":
    asyncio.run(main())
    