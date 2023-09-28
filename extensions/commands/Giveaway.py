import datetime
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from utils import DataManager


class GiveawayLeaveView(discord.ui.View):
    def __init__(self, giveaway_id, bot):
        super().__init__(timeout=None)
        self.giveaway_id = giveaway_id
        self.bot = bot

    @discord.ui.button(label="Leave Giveaway", style=discord.ButtonStyle.red)
    async def leave_giveaway(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if await DataManager.remove_giveaway_participant(
            self.giveaway_id, interaction.user.id
        ):
            await interaction.response.edit_message(
                content="You have successfully left the giveaway!", view=None
            )

            self.bot.dispatch("giveaway_leave", self.giveaway_id, interaction.guild.id)
        else:
            await interaction.response.edit_message(
                content="You have already left the giveaway!", view=None
            )


class GiveawayJoinView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(
        label="Join Giveaway",
        style=discord.ButtonStyle.green,
        custom_id="persistent_view:giveaway",
    )
    async def join_giveaway(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if await DataManager.add_giveaway_participant(
            interaction.message.id, interaction.user.id
        ):
            await interaction.response.send_message(
                content="Successfully entered the giveaway!", ephemeral=True
            )

            self.bot.dispatch(
                "giveaway_join",
                interaction.message.id,
                interaction.guild.id,
            )
        else:
            await interaction.response.send_message(
                content="You have already entered this giveaway!",
                ephemeral=True,
                view=GiveawayLeaveView(interaction.message.id, self.bot),
            )


class Giveaway(commands.GroupCog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="create", description="Create a giveaway")
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.guild.id))
    @app_commands.describe(
        time="How long the giveaway should last in minutes",
        winners="How many winners the giveaway should have",
        prize="What the prize of the giveaway is",
        channel="What channel the giveaway should be in",
        extra_notes="Any extra notes you want to add to the giveaway",
    )
    async def giveaway_create(
        self,
        interaction: discord.Interaction,
        time: int,
        winners: int,
        prize: str,
        channel: Optional[discord.TextChannel],
        extra_notes: Optional[str],
    ) -> None:
        if channel is None:
            channel = interaction.channel

        end_date = datetime.datetime.now() + datetime.timedelta(minutes=time)
        await interaction.response.send_message(
            f"Giveaway created in {channel.mention}!", ephemeral=True
        )

        message = await channel.send(
            embed=discord.Embed(
                title=f"{prize}",
                description=(f"{extra_notes}\n" if extra_notes is not None else "")
                + f"Ends: {discord.utils.format_dt(end_date, style='R')}\n"
                f"Hosted by: {interaction.user.mention}\n"
                f"Entries: **0**\n"
                f"Winners: **{winners}**",
            ),
            view=GiveawayJoinView(self.bot),
        )

        await DataManager.register_giveaway(
            message.id,
            interaction.guild.id,
            channel.id,
            time,
            winners,
            prize,
            extra_notes,
            interaction.user.id,
        )

    @app_commands.command(name="end", description="End a giveaway")
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.guild.id))
    @app_commands.describe(giveaway_id="The ID of the giveaway you want to end")
    async def giveaway_end(
        self, interaction: discord.Interaction, giveaway_id: str
    ) -> None:
        if giveaway_id.isnumeric():
            if await DataManager.get_giveaway_data(
                int(giveaway_id), interaction.guild.id
            ):
                giveaway_data = await DataManager.get_giveaway_data(
                    int(giveaway_id), interaction.guild.id
                )
                if giveaway_data["ended"]:
                    return await interaction.response.send_message(
                        f"Giveaway already ended!", ephemeral=True
                    )
                await DataManager.end_giveaway(int(giveaway_id), interaction.guild.id)
                await DataManager.edit_giveaway(
                    int(giveaway_id),
                    interaction.guild.id,
                    "end_date",
                    datetime.datetime.now().isoformat(),
                )
                self.bot.dispatch(
                    "manual_giveaway_end", int(giveaway_id), interaction.guild.id
                )
                await interaction.response.send_message(
                    f"Giveaway ended!", ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    f"Giveaway not found!", ephemeral=True
                )
        else:
            await interaction.response.send_message(
                f"Invalid giveaway ID!", ephemeral=True
            )

    @app_commands.command(name="reroll", description="Reroll a giveaway")
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.guild.id))
    @app_commands.describe(
        giveaway_id="The ID of the giveaway/giveaway winner you want to reroll"
    )
    async def giveaway_reroll(
        self,
        interaction: discord.Interaction,
        giveaway_id: str,
        user: Optional[discord.User],
    ) -> None:
        if giveaway_id.isnumeric():
            if await DataManager.get_giveaway_data(
                int(giveaway_id), interaction.guild.id
            ):
                giveaway_data = await DataManager.get_giveaway_data(
                    int(giveaway_id), interaction.guild.id
                )
                if giveaway_data["ended"]:
                    if user is None:
                        if len(giveaway_data["winners"]) > 0:
                            await DataManager.draw_giveaway_winners(
                                int(giveaway_id), interaction.guild.id
                            )
                            await interaction.response.send_message(
                                f"Giveaway rerolled!", ephemeral=True
                            )
                            self.bot.dispatch(
                                "manual_giveaway_reroll",
                                int(giveaway_id),
                                interaction.guild.id
                            )
                        else:
                            await interaction.response.send_message(
                                f"No winners to reroll!", ephemeral=True
                            )
                    else:
                        if user.id in giveaway_data["winners"]:
                            new_winner = await DataManager.replace_giveaway_winner(
                                int(giveaway_id), interaction.guild.id, user.id
                            )
                            await interaction.response.send_message(
                                f"Giveaway winner rerolled!", ephemeral=True
                            )
                            self.bot.dispatch(
                                "manual_giveaway_winner_reroll",
                                int(giveaway_id),
                                interaction.guild.id,
                                new_winner,
                            )
                        else:
                            await interaction.response.send_message(
                                f"User is not a winner!", ephemeral=True
                            )
                else:
                    await interaction.response.send_message(
                        f"Giveaway is still active!", ephemeral=True
                    )
            else:
                await interaction.response.send_message(
                    f"Giveaway not found!", ephemeral=True
                )
        else:
            await interaction.response.send_message(
                f"Invalid giveaway ID!", ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(Giveaway(bot))
