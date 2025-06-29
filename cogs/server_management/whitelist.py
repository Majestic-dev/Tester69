import discord
from discord.ext import commands

from discord import app_commands

from utils import data_manager

class whitelist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="whitelist", description="Add or remove an user from the whitelist"
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.choices(
        choice=[
            app_commands.Choice(name="Add", value="add"),
            app_commands.Choice(name="Remove", value="remove"),
        ]
    )
    @app_commands.describe(whitelist="The user to add or remove from the whitelist")
    async def whitelist(
        self,
        interaction: discord.Interaction,
        choice: app_commands.Choice[str],
        whitelist: discord.Member | discord.Role,
    ):
        if isinstance(whitelist, discord.Role):
            if whitelist >= interaction.user.top_role:
                return await interaction.response.send_message(
                    ephemeral=True,
                    embed=discord.Embed(
                        description=(f"<:white_cross:1096791282023669860> Could not ")
                        + (
                            f"add {whitelist.mention} role to "
                            if choice.value == "add"
                            else f"remove {whitelist.mention} role from "
                        )
                        + ("the whitelist because it's higher than your highest role"),
                        colour=discord.Colour.orange(),
                    ),
                )
        elif isinstance(whitelist, discord.Member):
            user = interaction.guild.get_member(whitelist.id)
            if user.top_role >= interaction.user.top_role and user != interaction.user:
                return await interaction.response.send_message(
                    ephemeral=True,
                    embed=discord.Embed(
                        description=(f"<:white_cross:1096791282023669860> Could not ")
                        + (
                            f"add {whitelist.mention} to "
                            if choice.value == "add"
                            else f"remove {whitelist.mention} from "
                        )
                        + (
                            "the whitelist because their highest role is higher than yours"
                        ),
                        colour=discord.Colour.orange(),
                    ),
                )
        else:
            pass

        guild_filtered_words_data = await data_manager.get_filter_data(
            interaction.guild.id
        )
        wlist = guild_filtered_words_data["whitelist"]

        if choice.value == "add":
            if wlist is None or whitelist.id not in wlist:
                wlist.append(whitelist.id)
                await data_manager.edit_filter_data(
                    interaction.guild.id, "whitelist", wlist
                )
                await interaction.response.send_message(
                    ephemeral=True,
                    embed=discord.Embed(
                        description=f"<:white_checkmark:1096793014287995061> Added {whitelist.mention} to the whitelist",
                        colour=discord.Colour.green(),
                    ),
                )

            elif whitelist.id in wlist:
                return await interaction.response.send_message(
                    ephemeral=True,
                    embed=discord.Embed(
                        description=f"<:white_cross:1096791282023669860> Could not add {whitelist.mention} to the whitelist because they are already in the whitelist",
                        colour=discord.Colour.orange(),
                    ),
                )

        elif choice.value == "remove":
            if wlist is None or whitelist.id not in wlist:
                return await interaction.response.send_message(
                    ephemeral=True,
                    embed=discord.Embed(
                        description=f"<:white_cross:1096791282023669860> Could not remove {whitelist.mention} from the whitelist because they are not in the whitelist",
                        colour=discord.Colour.orange(),
                    ),
                )

            elif whitelist.id in wlist:
                wlist.remove(whitelist.id)
                await data_manager.edit_filter_data(
                    interaction.guild.id, "whitelist", wlist
                )
                await interaction.response.send_message(
                    ephemeral=True,
                    embed=discord.Embed(
                        description=f"<:white_checkmark:1096793014287995061> Removed {whitelist.mention} from the whitelist",
                        colour=discord.Colour.green(),
                    ),
                )

    @app_commands.command(
        name="list_whitelist", description="List all whitelisted users and/or roles"
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    async def list_whitelist(self, interaction: discord.Interaction):
        guild_filtered_words_data = await data_manager.get_filter_data(
            interaction.guild.id
        )
        wlist = guild_filtered_words_data["whitelist"]

        if wlist is None or len(wlist) == 0:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description=f"<:white_cross:1096791282023669860> There are no whitelisted users or roles in this server",
                    colour=discord.Colour.orange(),
                )
            )

        role_list = []
        user_list = []

        for i in wlist:
            role = interaction.guild.get_role(i)
            member = interaction.guild.get_member(i)

            if role:
                role_list.insert(0, role)
            elif member:
                user_list.insert(0, member)

        role_list = sorted(role_list, key=lambda r: r.position, reverse=True)
        user_list = sorted(user_list, key=lambda u: u.name, reverse=True)

        wlist = [r.mention for r in role_list] + [u.mention for u in user_list]

        await interaction.response.send_message(
            embed=discord.Embed(
                description=f"Whitelisted users and/or roles in this server:\n\n{',\n'.join(wlist)}",
                colour=discord.Colour.green(),
            ),
            ephemeral=True,
        )

async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(whitelist(bot))