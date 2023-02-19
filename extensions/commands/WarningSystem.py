import json
import os
import uuid
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands


class WarningSystem(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def registerWarning(self, id, reason, content):
        if f"{id}.json" in os.listdir("./data/"):
            with open(f"./data/{id}.json", "r") as r:
                d8a = json.load(r)

            x = {f"{uuid.uuid4()}": {"reason": reason, "content": content}}

            d8a["warnings"].update(x)
            with open(f"./data/{id}.json", "w") as w:
                json.dump(d8a, w, indent=4)

        else:
            with open(f"./data/{id}.json", "w") as w:
                d8a = {
                    "warnings": {
                        f"{uuid.uuid1()}": {"reason": reason, "content": content}
                    },
                }

                json.dump(d8a, w, indent=4)

    @app_commands.command(
        name="warn", description="Warns the mentioned user with a custom warning reason"
    )
    @commands.has_permissions(manage_messages=True)
    async def warn(
        self, interaction: discord.Interaction, user: discord.User, *, reason: str
    ):
        user_id = str(user.id)
        self.registerWarning(
            user_id, reason, f"Warned by {interaction.user} on {datetime.now()}"
        )

        warn = discord.Embed(
            title="Warning",
            description=(f"{user.name} has been warned for: ```{reason}```"),
            timestamp=datetime.now(),
            colour=discord.Colour.red(),
        )
        await interaction.response.send_message(embed=warn)

    @app_commands.command(name="delwarn", description="Deletes the warning by UUID")
    @commands.has_permissions(manage_messages=True)
    async def delwarn(self, interaction: discord.Interaction, uuid: str):
        found = False

        DeletedWarning = discord.Embed(
            title="Warning Deleted",
            description=(f"Deleted warning ```{uuid}```"),
            timestamp=datetime.now(),
            colour=discord.Colour.green(),
        )

        NotFound = discord.Embed(
            title="Not Found",
            description=(f"Couldn't find ```{uuid}```"),
            timestamp=datetime.now(),
            colour=discord.Colour.orange(),
        )

        WarningNotFound = discord.Embed(
            title="Warning Not Found",
            description=(f"Couldn't find warning ID ```{uuid}```"),
            timestamp=datetime.now(),
            colour=discord.Colour.orange(),
        )

        for file in os.listdir("./data/"):
            if file == "users.json":
                continue
            with open(f"./data/{file}", "r") as r:
                d8a = json.load(r)

            if uuid in d8a["warnings"]:
                del d8a["warnings"][uuid]

                with open(f"./data/{file}", "w") as w:
                    json.dump(d8a, w, indent=4)

                await interaction.response.send_message(embed=DeletedWarning)
                found = True

            elif uuid not in d8a["warnings"]:
                await interaction.response.send_message(embed=NotFound)

        if found != True:
            interaction.response.send_message(embed=WarningNotFound)

    @app_commands.command(
        name="warnings", description="get the warning list of the user"
    )
    @commands.has_permissions(manage_messages=True)
    async def warnings(self, interaction: discord.Interaction, member: discord.Member):

        if f"{member.id}.json" in os.listdir("./data/"):

            e = discord.Embed(title="Warnings", 
                              timestamp=datetime.now(),
                              colour=discord.Colour.orange())

            with open(f"./data/{member.id}.json", "r") as r:
                d8a = json.load(r)

            warnings = d8a["warnings"]

            if len(d8a["warnings"]) == 0:
                e = discord.Embed(
                    title="Warnings",
                    description=f"{member.mention} has no warnings",
                    timestamp=datetime.now(),
                    colour=discord.Colour.green(),
                )

                e.set_author(name=member.name, icon_url=member.avatar.url)

                await interaction.response.send_message(embed=e)
                return

            for warning in warnings:
                e.add_field(
                    name=warning,
                    value="Reason: "
                    + warnings[warning]["reason"]
                    + "\nContent: "
                    + warnings[warning]["content"],
                    inline=False,
                )

            e.set_author(name=member.name, icon_url=member.avatar.url)
            await interaction.response.send_message(embed=e)

        else:
            e = discord.Embed(
                title="Warnings",
                description=f"{member.mention} has no warnings",
                timestamp=datetime.now(),
                colour=discord.Colour.green(),
            )

            e.set_author(name=member.name, icon_url=member.avatar.url)

            await interaction.response.send_message(embed=e)

    @commands.Cog.listener()
    async def on_message(self, message):
        content = message.content.lower()

        if "https" in content:
            await message.delete()
            e = discord.Embed(
                title="Warning",
                description=f"{message.author.mention} has been warned for posting a link",
                timestamp=datetime.now(),
                colour=discord.Colour.red(),
            )

            await message.channel.send(embed=e)
            self.registerWarning(
                id=message.author.id, reason="Posting a link", content=content
            )

        elif "http" in content:
            await message.delete()
            e = discord.Embed(
                title="Warning",
                description=f"{message.author.mention} has been warned for posting a link",
                timestamp=datetime.now(),
                colour=discord.Colour.red(),
            )

            await message.channel.send(embed=e)
            self.registerWarning(
                id=message.author.id, reason="Posting a link", content=content
            )

        elif "discord.gg" in content:
            await message.delete()
            e = discord.Embed(
                title="Warning",
                description=f"{message.author.mention} has been warned for posting a link",
                timestamp=datetime.now(),
                colour=discord.Colour.red(),
            )

            await message.channel.send(embed=e)
            self.registerWarning(
                id=message.author.id, reason="Posting a link", content=content
            )

        elif ".com" in content:
            await message.delete()
            e = discord.Embed(
                title="Warning",
                description=f"{message.author.mention} has been warned for posting a link",
                timestamp=datetime.now(),
                colour=discord.Colour.red(),
            )

            await message.channel.send(embed=e)
            self.registerWarning(
                id=message.author.id, reason="Posting a link", content=content
            )

        elif "uwu" in content:
            await message.delete()
            e = discord.Embed(
                title="Warning",
                description=f'{message.author.mention} has been warned for posting "uwu"',
                timestamp=datetime.now(),
                colour=discord.Colour.red(),
            )

            await message.channel.send(embed=e)
            self.registerWarning(
                id=message.author.id, reason='Posting "uwu"', content=content
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(WarningSystem(bot))