from discord.ext import commands
import discord

class MainStuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):

        Ping = discord.Embed(
            title = "Pong!",
            description = f"🏓 My ping is {round(self.bot.latency * 1000)}ms 🏓",
            colour = discord.Colour.green())

        await ctx.reply(embed = Ping)

    @commands.command()
    async def prefix(self, ctx):

        Prefix = discord.Embed(
            title = "Prefix",
            description = "Tester69's prefix is `'`",
            colour = discord.Colour.light_gray())

        await ctx.reply(embed = Prefix)

    @commands.command()
    async def help(self, ctx):

        help = discord.Embed(
            title = "Tetser69's command list",
            colour = discord.Colour.light_gray())
        
        help.add_field(
            name = "Moderation", value = "`'moderation`", inline=True)
        help.add_field(
            name = "Economy", value = "`'economy`")
        
        await ctx.reply(embed = help)

    @commands.command()
    async def moderation(self, ctx):

        moderation = discord.Embed(
            title = "Tester69's moderation commands",
            colour = discord.Colour.darker_gray())
        moderation.add_field(
            name = "Kick", value = "`'kick`", inline = True)
        moderation.add_field(
            name = "Mute", value = "`'mute`", inline = True)
        moderation.add_field(
            name = "Unmute", value = "`'unmute`", inline = True)
        moderation.add_field(
            name = "RandomBan", value = "`'randomban`", inline = True)
        moderation.add_field(
            name = "Ban", value = "`'ban`", inline = True)
        moderation.add_field(
            name = "Unban", value = "`'unban`", inline = True)
        moderation.add_field(
            name = "Warn", value = "`'warn`", inline = True)
        moderation.add_field(
            name = "Delwarn", value = "`'delwarn`", inline = True)

        await ctx.reply(embed = moderation)

    @commands.command()
    async def economy(self, ctx):

        economy = discord.Embed(
            title = "Tester69's economy commands",
            colour = discord.Colour.darker_grey())
        economy.add_field(
            name = "Add", value = "`'add`", inline = True)
        economy.add_field(
            name = "Subtract", value = "`'subtract`", inline = True)
        economy.add_field(
            name = "Balance", value = "`'balance`", inline = True)
        economy.add_field(
            name = "Inventory", value = "`'inventory`", inline = True)
        economy.add_field(
            name = "Fish", value = "`'fish`", inline = True)
        economy.add_field(
            name = "Hourly", value = "`'hourly`", inline = True)
        economy.add_field(
            name = "Sell", value = "`'sell`", inline = True)
        economy.add_field(
            name = "Gamble", value = "`'gamble`", inline = True)
            
        await ctx.reply(embed = economy)

async def setup(bot):
   await bot.add_cog(MainStuff(bot))