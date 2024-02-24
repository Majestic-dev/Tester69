import discord
from discord import app_commands
from discord.ext import commands


class help_select(discord.ui.Select):
    def __init__(self, bot: commands.AutoShardedBot):
        super().__init__(
            placeholder="Choose a command category",
            options=[
                discord.SelectOption(label=cog_name, description=cog.__doc__)
                for cog_name, cog in bot.cogs.items()
                if cog.__cog_app_commands__
                and cog_name not in ["HelpSelect", "Gambling"]
            ],
        )

        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        cog = self.bot.get_cog(self.values[0])
        assert cog

        commands_mixer = []
        for i in cog.walk_app_commands():
            commands_mixer.append(i)

        embed = discord.Embed(
            title=f"{cog.__cog_name__} Commands",
            description="\n".join(
                f"* **/{command.name}:** `{command.description}`\n"
                for command in commands_mixer
            ),
            colour=discord.Colour.light_gray(),
        ).set_footer(
            text=f"{len(commands_mixer)} {cog.__cog_name__} Commands | Credits to: CodeWithPranoy on Youtube"
        )

        view = discord.ui.View().add_item(help_select(self.bot))
        await interaction.response.edit_message(embed=embed, view=view)


class main_stuff(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @app_commands.command(name="help", description="Get the basic help for commands")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Help Command",
            description="Choose a slash command category you need help for",
            colour=discord.Colour.light_gray(),
        )

        view = discord.ui.View().add_item(help_select(self.bot))
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @app_commands.command(name="ping", description="Show my ping")
    async def ping(self, interaction: discord.Interaction):
        Ping = discord.Embed(
            title="Pong!",
            description=f"🏓 My ping is {round(self.bot.latency * 1000)}ms 🏓",
            colour=discord.Colour.green(),
        )

        await interaction.response.send_message(embed=Ping, ephemeral=True)


async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(main_stuff(bot))
