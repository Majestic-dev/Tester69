from discord.ext import commands
from datetime import datetime
import discord
import json
import uuid
import random
import os

class WarningSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def registerWarning(self, id, reason, content):

        if f"{id}.json" in os.listdir("./data/"):
            with open(f"./data/{id}.json", "r") as r:
                d8a = json.load(r)

            x = {f"{uuid.uuid4()}" : {"reason" : reason, "content" : content}}

            d8a["warnings"].update(x)
            with open(f"./data/{id}.json", "w") as w:
                json.dump(d8a, w, indent=4)

        else:
            with open(f"./data/{id}.json", "w") as w:
                d8a = {
                    "warnings" : {
                        f"{uuid.uuid1()}": {"reason" : reason, "content" : content}
                    },
                }

                json.dump(d8a, w, indent=4)

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def warn(self, ctx, user: discord.User, *, reason: str):
        user_id = str(user.id)
        self.registerWarning(user_id, reason, f"Warned by {ctx.author.name} on {datetime.now()}")

        warn = discord.Embed(
            title = "Warning",
            description = (f"{user.name} has been warned for: ```{reason}```"),
            colour = discord.Colour.red())
        await ctx.reply(embed = warn)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def delwarn(self, ctx, uuid):
        found = False

        DeletedWarning = discord.Embed(
            title = "Warning Deleted",
            description = (f"Deleted warning ```{uuid}```"),
            colour = discord.Colour.green())

        NotFound = discord.Embed(
            title = "Not Found",
            description = (f"Couldn't find ```{uuid}```"),
            colour = discord.Colour.orange())

        WarningNotFound = discord.Embed(
            title = "Warning Not Found",
            description = (f"Couldn't find warning ID ```{uuid}```"),
            colour = discord.Colour.orange())

        for file in os.listdir("./data/"):
            if file == "users.json":
                continue
            with open(f"./data/{file}", "r") as r:
                d8a = json.load(r)

            if uuid in d8a["warnings"]:
                del d8a["warnings"][uuid]

                with open(f"./data/{file}", "w") as w:
                    json.dump(d8a, w, indent=4)

                await ctx.reply(embed = DeletedWarning)
                found = True

            elif uuid not in d8a["warnings"]:
                await ctx.reply(embed = NotFound)

        if found != True:
            ctx.reply(embed = WarningNotFound)

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def warnings(self, ctx, member : discord.Member):

        if f"{member.id}.json" in os.listdir("./data/"):

            e = discord.Embed(
                title = "Warnings",
                colour = discord.Colour.orange())

            with open(f"./data/{member.id}.json", "r") as r:
                d8a = json.load(r)

            warnings = d8a["warnings"]

            if len(d8a["warnings"]) == 0:
                e = discord.Embed(
                title = "Warnings",
                description = f"{member.mention} has no warnings",
                colour = discord.Colour.green())

                e.set_author(name = member.name, icon_url = member.avatar_url)

                await ctx.reply(embed=e)
                return

            for warning in warnings:
                e.add_field(
                    name = warning,
                    value = "Reason: " + warnings[warning]["reason"] + "\nContent: " + warnings[warning]["content"],
                    inline = False)

            e.set_author(name = member.name, icon_url = member.avatar_url)
            await ctx.reply(embed=e)

        else:
            e = discord.Embed(
                title = "Warnings",
                description = f"{member.mention} has no warnings",
                colour = discord.Colour.green())

            e.set_author(name = member.name, icon_url = member.avatar_url)

            await ctx.reply(embed=e)

    @commands.Cog.listener()
    async def on_message(self, message):
        content = message.content.lower()

        if "https" in content:
                await message.delete()
                e = discord.Embed(
                    title = "Warning",
                    description = f"{message.author.mention} has been warned for posting a link",
                    colour = discord.Colour.red())

                await message.channel.send(embed=e)
                self.registerWarning(id = message.author.id, reason = "Posting a link", content = content)

        elif "http" in content:
                await message.delete()
                e = discord.Embed(
                    title = "Warning",
                    description = f"{message.author.mention} has been warned for posting a link",
                    colour = discord.Colour.red())

                await message.channel.send(embed=e)
                self.registerWarning(id = message.author.id, reason = "Posting a link", content = content)

        elif "discord.gg" in content:
                await message.delete()
                e = discord.Embed(
                    title = "Warning",
                    description = f"{message.author.mention} has been warned for posting a link",
                    colour = discord.Colour.red())

                await message.channel.send(embed=e)
                self.registerWarning(id = message.author.id, reason = "Posting a link", content = content)

        elif ".com" in content:
                await message.delete()
                e = discord.Embed(
                    title = "Warning",
                    description = f"{message.author.mention} has been warned for posting a link",
                    colour = discord.Colour.red())

                await message.channel.send(embed=e)
                self.registerWarning(id = message.author.id, reason = "Posting a link", content = content)

        elif "uwu" in content:
                await message.delete()  
                e = discord.Embed(
                    title = "Warning",
                    description = f"{message.author.mention} has been warned for posting \"uwu\"",
                    colour = discord.Colour.red())

                await message.channel.send(embed=e)
                self.registerWarning(id = message.author.id, reason = "Posting \"uwu\"", content = content)

def setup(bot):
    bot.add_cog(WarningSystem(bot))