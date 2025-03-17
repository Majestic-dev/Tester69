import discord
from discord import app_commands
from discord.ext import commands

from utils import data_manager


class leaderboard_dropdown(discord.ui.Select):
    def __init__(self, bot: commands.AutoShardedBot, interaction: discord.Interaction):
        self.bot = bot
        self.executer = interaction.user.id

        options = [
            discord.SelectOption(
                label="Cash",
                value="cash",
                description="Cash Balance Leaderboard",
                emoji="💵",
            ),
            discord.SelectOption(
                label="Bank",
                value="bank",
                description="Bank Balance Leaderboard",
                emoji="🏦",
            ),
        ]
        super().__init__(
            placeholder="Choose a leaderboard type",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.executer:
            return await interaction.response.send_message(
                ephemeral=True,
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> This isn't yours",
                    colour=discord.Colour.red(),
                ),
            )

        if self.values[0] == "cash":
            user_ids = await data_manager.get_all_users()
            users = {
                user_id: await data_manager.get_user_data(user_id)
                for user_id in user_ids
            }
            top_10 = sorted(users, key=lambda k: users[k]["balance"], reverse=True)[:10]

            lb_embed = discord.Embed(
                colour=discord.Colour.green(),
            )

            for i, user in enumerate(top_10):
                lb_embed.add_field(
                    name=f"{i + 1}. {self.bot.get_user(int(user))}",
                    value=f"**Wallet:** `{users[user]['balance']}` 🪙",
                    inline=False,
                )

            lb_embed.set_author(name="Cash Leaderboard", icon_url=self.bot.user.avatar)
            await interaction.response.edit_message(
                content=None,
                embed=lb_embed,
                view=leaderboard_dropdown_view(bot=self.bot, interaction=interaction),
            )

        elif self.values[0] == "bank":
            user_ids = await data_manager.get_all_users()
            users = {
                user_id: await data_manager.get_user_data(user_id)
                for user_id in user_ids
            }
            top_10 = sorted(users, key=lambda k: users[k]["bank"], reverse=True)[:10]

            lb_embed = discord.Embed(
                colour=discord.Colour.green(),
            )

            for i, user in enumerate(top_10):
                lb_embed.add_field(
                    name=f"{i + 1}. {self.bot.get_user(int(user))}",
                    value=f"**Bank:** `{users[user]['bank']}` 🪙",
                    inline=False,
                )

            lb_embed.set_author(name="Bank Leaderboard", icon_url=self.bot.user.avatar)
            await interaction.response.edit_message(
                embed=lb_embed,
                view=leaderboard_dropdown_view(bot=self.bot, interaction=interaction),
            )


class leaderboard_dropdown_view(discord.ui.View):
    def __init__(self, bot: commands.AutoShardedBot, interaction: discord.Interaction):
        self.bot = bot
        super().__init__()

        self.add_item(leaderboard_dropdown(bot=self.bot, interaction=interaction))


class leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="leaderboard", description="See the top 10 richest people"
    )
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    @app_commands.choices(
        choices=[
            app_commands.Choice(name="💵 Cash", value="cash"),
            app_commands.Choice(name="🏦 Bank", value="bank"),
        ]
    )
    @app_commands.describe(choices="The type of leaderboard you want to see")
    async def leaderboard(
        self, interaction: discord.Interaction, choices: app_commands.Choice[str]
    ):
        view = leaderboard_dropdown_view(bot=self.bot, interaction=interaction)

        if choices.value == "cash":
            user_ids = await data_manager.get_all_users()
            users = {
                user_id: await data_manager.get_user_data(user_id)
                for user_id in user_ids
            }
            top_10 = sorted(users, key=lambda k: users[k]["balance"], reverse=True)[:10]

            lb_embed = discord.Embed(
                colour=discord.Colour.green(),
            )

            for i, user in enumerate(top_10):
                lb_embed.add_field(
                    name=f"{i + 1}. {self.bot.get_user(int(user))}",
                    value=f"**Wallet:** `{users[user]['balance']}` 🪙",
                    inline=False,
                )

            lb_embed.set_author(name="Cash Leaderboard", icon_url=self.bot.user.avatar)
            await interaction.response.send_message(embed=lb_embed, view=view)

        elif choices.value == "bank":
            user_ids = await data_manager.get_all_users()
            users = {
                user_id: await data_manager.get_user_data(user_id)
                for user_id in user_ids
            }
            top_10 = sorted(users, key=lambda k: users[k]["bank"], reverse=True)[:10]

            lb_embed = discord.Embed(
                colour=discord.Colour.green(),
            )

            for i, user in enumerate(top_10):
                lb_embed.add_field(
                    name=f"{i + 1}. {self.bot.get_user(int(user))}",
                    value=f"**Bank:** `{users[user]['bank']}` 🪙",
                    inline=False,
                )

            lb_embed.set_author(name="Bank Leaderboard", icon_url=self.bot.user.avatar)
            await interaction.response.send_message(embed=lb_embed, view=view)