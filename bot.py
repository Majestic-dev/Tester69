from discord.ext import commands
from typing import Literal, Optional
from discord.ext import commands
from discord.ext.commands import Greedy, Context
import json
import os
import discord
from dotenv import load_dotenv
load_dotenv()

if not os.path.isfile("data/users.json"):
    with open("data/users.json", "w") as f:
        json.dump({}, f)

Start = discord.Embed(
        title = "ERROR",
        description = "You need to execute the `'start` command before executing any other commands",
        colour = discord.Colour.dark_orange())

intents = discord.Intents.all()
intents.members = True
whitelist = ["705435835306213418"]
owners = [705435835306213418]

bot_prefix = "'"
bot = commands.Bot(command_prefix = bot_prefix, intents = intents)
bot.remove_command("help")


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(f"'help - https://discord.gg/VsDDf8YKBV"))
    await bot.load_extension("extensions.commands.MainStuff")
    await bot.load_extension("extensions.commands.WarningSystem")
    await bot.load_extension("extensions.commands.Moderation")
    await bot.load_extension("extensions.commands.Economy")
    await bot.load_extension("extensions.commands.Gambling")

@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
  ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

users = {}

try:
    with open('data/users.json', 'r') as f:
        users = json.load(f)
except:
    print('Could not load data')

def save_data():
    with open('data/users.json', 'w') as f:
        json.dump(users, f, indent=4)

""""
@bot.command()
async def bj(ctx, bet: int):
    player_cards = []
    dealer_cards = []
    player_score = 0
    dealer_score = 0
    user_id = str(ctx.author.id)
    with open("data/users.json", "r") as f:
        data = json.load(f)
    if user_id not in data:
        await ctx.send(embed = Start)
        return
    if bet > data[user_id]['balance']:

        NoCoins = discord.Embed(
            title = "Not Enough Coins", 
            description = "You don't have enough coins.", 
            color = discord.Color.orange())
        await ctx.send(embed = NoCoins)

        return
    data[user_id]['balance'] -= bet
    for i in range(2):
        card = random.randint(1, 11)
        player_cards.append(card)
        player_score += card
        card = random.randint(1, 11)
        dealer_cards.append(card)
        dealer_score += card

    YourCards = discord.Embed(
        title = "Your Cards And Score", 
        description = f"Cards: {player_cards}\nScore: {player_score}", 
        color = discord.Color.dark_grey())

    await ctx.send(embed = YourCards)
    while player_score < 21:
        action = await bot.wait_for("message", check = lambda message: message.author == ctx.author)
        if action.content.lower() == "hit":
            card = random.randint(1, 11)
            player_cards.append(card)
            player_score += card

            YourCards2 = discord.Embed(
                title = "Your Cards And Score", 
                description = f"Cards: {player_cards}\nScore: {player_score}", 
                color = discord.Color.darker_grey())

            await ctx.send(embed = YourCards2)
        elif action.content.lower() == "stand":
            break
        else:

            InvalidAction = discord.Embed(
                title = "Error", 
                description = "Invalid action. Please type 'hit' or 'stand'.", 
                color = discord.Color.red())

            await ctx.send(embed = InvalidAction)
        
    while dealer_score < 17:
        dealer_card = random.randint(1, 11)
        dealer_cards.append(dealer_card)
        dealer_score += dealer_card
    if player_score > 21:

        PlayerBust = discord.Embed(
            title = "You Lose!", 
            description = f"Your score: {player_score}\nDealer's cards: {dealer_cards}\nDealer's score: {dealer_score}", 
            color = discord.Color.red())

        await ctx.send(embed = PlayerBust)
        data[user_id]['balance'] -= bet
    elif dealer_score > 21:

        DealerBust = discord.Embed(
        title = "You Win!", 
        description = f"Your score: {player_score}\nDealer's cards: {dealer_cards}\nDealer's score: {dealer_score}", 
        color = discord.Color.green())

        await ctx.send(embed = DealerBust)
        data[user_id]['balance'] += bet
    elif dealer_score > player_score:

        PlayerLost = discord.Embed(
            title = "You Lose!", 
            description = f"Your score: {player_score}\nDealer's cards: {dealer_cards}\nDealer's score: {dealer_score}", 
            color = discord.Color.red())

        await ctx.send(embed = PlayerLost)
        data[user_id]['balance'] -= bet
    elif dealer_score < player_score:

        PlayerWon = discord.Embed(
            title = "You Win!", 
            description = f"Your score: {player_score}\nDealer's cards: {dealer_cards}\nDealer's score: {dealer_score}", 
            color = discord.Color.green())

        await ctx.send(embed = PlayerWon)
        data[user_id]['balance'] += bet
    else:

        PlayerTie = discord.Embed(
            title = "Tie!", 
            description = f"Your score: {player_score}\nDealer's cards: {dealer_cards}\nDealer's score: {dealer_score}", 
            color = discord.Color.blue())

        await ctx.send(embed = PlayerTie)
    with open("data/users.json", "w") as f:
        json.dump(data, f, indent=4)
"""

bot.run(os.getenv('TOKEN'))