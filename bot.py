from discord.ext import commands
from discord.ext.commands import has_permissions
from datetime import datetime, timedelta
from datetime import datetime
#from discord import app_commands
#soon slash commands...
import json
import os
import discord
import uuid
import random
import time

if not os.path.isfile("data/users.json"):
    with open("data/users.json", "w") as f:
        json.dump({}, f)

Start = discord.Embed(
        title = "ERROR",
        description = "You need to execute the `'start` command before executing any other commands",
        colour = discord.Colour.dark_orange())

intents = discord.Intents.default()
intents.members = True
whitelist = ["705435835306213418"]

bot_prefix = "'"
bot = commands.Bot(command_prefix = bot_prefix, intents = intents)
bot.remove_command("help")

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(f"'help - https://discord.gg/VsDDf8YKBV"))

@bot.command()
async def ping(ctx):
    await ctx.reply(f"Pong! My ping is currently {round(bot.latency * 1000)}ms")

@bot.command()
async def prefix(ctx):
    await ctx.reply("Tester69's prefix is `'`")

@bot.command()
async def help(ctx):
    help = discord.Embed(
        title = "Tetser69's command list",
        colour = discord.Colour.light_gray())
        
    help.add_field(
        name = "Moderation", value = "`'moderation`", inline=True)
    help.add_field(
        name = "Economy", value = "`'economy`")
    await ctx.reply(embed = help)

@bot.command()
async def moderation(ctx):
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

@bot.command()
async def economy(ctx):
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

#Basic shit above

#Warning system below

def registerWarning(id, reason, content):

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

@bot.command()
async def warn(ctx, user: discord.User, *, reason: str):
    user_id = str(user.id)
    registerWarning(user_id, reason, f"Warned by {ctx.author.name} on {datetime.now()}")

    warn = discord.Embed(
        title = "Warning",
        description = (f"{user.name} has been warned for: ```{reason}```"),
        colour = discord.Colour.red())
    await ctx.reply(embed = warn)

def registerWarning(id, reason, content):
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

@bot.command()
@has_permissions(manage_messages=True)
async def delwarn(ctx, uuid):
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
        await ctx.reply(embed = WarningNotFound)

@bot.command()
@has_permissions(manage_messages=True)
async def warnings(ctx, member : discord.Member):
    
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

@bot.event
async def on_message(message):
    content = message.content.lower()

    #if message.author.id == 705435835306213418:
        #return

    if "https" in content:
            await message.delete()
            e = discord.Embed(
        title = "Warning",
        description = f"{message.author.mention} has been warned for posting a link",
        colour = discord.Colour.red())

            await message.channel.reply(embed=e)
            registerWarning(id = message.author.id, reason = "Posting a link", content = content)

    elif "http" in content:
            await message.delete()
            e = discord.Embed(
        title = "Warning",
        description = f"{message.author.mention} has been warned for posting a link",
        colour = discord.Colour.red())

            await message.channel.reply(embed=e)
            registerWarning(id = message.author.id, reason = "Posting a link", content = content)

    elif "discord.gg" in content:
            await message.delete()
            e = discord.Embed(
        title = "Warning",
        description = f"{message.author.mention} has been warned for posting a link",
        colour = discord.Colour.red())

            await message.channel.reply(embed=e)
            registerWarning(id = message.author.id, reason = "Posting a link", content = content)

    elif ".com" in content:
            await message.delete()
            e = discord.Embed(
        title = "Warning",
        description = f"{message.author.mention} has been warned for posting a link",
        colour = discord.Colour.red())

            await message.channel.reply(embed=e)
            registerWarning(id = message.author.id, reason = "Posting a link", content = content)

    elif "uwu" in content:
            await message.delete()  
            e = discord.Embed(
        title = "Warning",
        description = f"{message.author.mention} has been warned for posting \"uwu\"",
        colour = discord.Colour.red())

            await message.channel.reply(embed=e)
            registerWarning(id = message.author.id, reason = "Posting \"uwu\"", content = content)
        
    await bot.process_commands(message)

#Warning system above

#Moderation commands below

@bot.command()
@has_permissions(ban_members=True)
async def randomban(ctx):
    whitelist = [ 705435835306213418 ]

    if ctx.guild.id == 733219077744754750:
        return  

    if ctx.author.id in whitelist:
        random_ = random.randint(0, len(ctx.guild.members))
        member_id = ctx.guild.members[random_].id

        
        for member in ctx.guild.members:
            if member.id == member_id:
                await ctx.reply(f"{member} will be banned, are you sure you'd like to ban them? Execute `'confirm` command to apply ban.")

                with open("./data/randomMember.json", "w") as w:
                    dataStruct = {
                        "member_id" : member_id
                    }

                    json.dump(dataStruct, w, indent=4)

@bot.command()
@has_permissions(ban_members=True)
async def confirm(ctx):

    if ctx.author.id in whitelist:

        with open("./data/randomMember.json", "r") as r:
            member_id = json.load(r)["member_id"]

        for member in ctx.guild.members:
            if member.id == member_id:
                await member.ban(reason = "Random ban")
                await ctx.reply(f"Successfuly banned {member}")
                break

@bot.command()
@has_permissions(kick_members = True)
async def mute(ctx, member : discord.Member = None, *, reason = "Unspecified"):
    if member == None:
        Mute = discord.Embed(
            title = "Mute",
            description = "Mutes the user by their discord user ID \n Example: `'Mute 705435835306213418 Not cool`",
            colour = discord.Colour.light_gray())

        await ctx.reply(embed = Mute)

    else:

        MuteA = discord.Embed(
            title = ":warning: Error :warning:",
            description = (f"Could not mute {member} because they are already muted"),
            colour = discord.Colour.dark_orange())

        MuteB = discord.Embed(
            title = ":white_check_mark: Mute Successful :white_check_mark:",
            description = (f"Successfully muted {member}"),
            colour = discord.Colour.red())

        role = discord.utils.get(ctx.guild.roles, name = "muted")

        if role in member.roles:
            await ctx.reply(embed = MuteA)
        else:
            await member.add_roles(role)
            await ctx.reply(embed = MuteB)

@bot.command()
@has_permissions(kick_members = True)
async def unmute(ctx, member : discord.Member = None):
    if member == None:
        Unmute = discord.Embed(
            title = "Unmute",
            description = "Unmutes the user by their discord user ID \n Example: `'Unmute 705435835306213418 Very cool`",
            colour = discord.Colour.light_gray())

        await ctx.reply(embed = Unmute)

    else:

        UnmuteA = discord.Embed(
            title = ":warning: Error :warning:",
            description = (f"Could not unmute {member} because they are not muted"),
            colour = discord.Colour.dark_orange())

        UnmuteB = discord.Embed(
            title = ":white_check_mark: Unmute Successful :white_check_mark:",
            description = (f"Successfully unmuted {member}"),
            colour = discord.Colour.green())

        role = discord.utils.get(ctx.guild.roles, name = "muted")

        if role in member.roles:
            await member.remove_roles(role)
            await ctx.reply(embed = UnmuteB)
        else:
            await ctx.reply(embed = UnmuteA)

@bot.command()
@has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member = None, *, reason = "Unspecified"):
    if member == None:
        Kick = discord.Embed(
            title = "Kick",
            description = "kicks the user by their discord user ID \n Example: `'Kick 705435835306213418 Not cool`",
            colour = discord.Colour.light_gray())

        await ctx.reply(embed = Kick)

    else:

        KickA = discord.Embed(
            title = ":white_check_mark: Kick Successful :white_check_mark:",
            description = (f"Successfully kicked {member}"),
            colour = discord.Colour.red())

        KickB = discord.Embed(
            title = ":warning: Error :warning:",
            description = (f"Couldn't kick {member}, they might be higher than me or not in the server"),
            colour = discord.Colour.dark_orange())

        if member.id == ctx.author.id:
            await ctx.reply("You cannot kick yourself!")

        else:
            try:
                await member.kick(reason=reason)
                await ctx.reply(embed = KickA)
            except:
                await ctx.reply(embed = KickB)

@bot.command()
@has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member = None, *, reason = "Unspecified"):
    if member == None:

        Ban = discord.Embed(
            title = "Ban",
            description = "Bans the user by their discord user ID \n Example: `'ban 705435835306213418 Not cool`",
            colour = discord.Colour.light_gray())

        await ctx.reply(embed = Ban)

    else:

        BanA = discord.Embed(
            title = ":white_check_mark: Ban Successful :white_check_mark:",
            description = (f"Successfully banned {member}"),
            colour = discord.Colour.red())

        BanB = discord.Embed(
            title = ":warning: Error :warning:",
            description = (f"Could not ban {member}, they might be higher than me or not in the server"),
            colour = discord.Colour.dark_orange())

        if member.id == ctx.author.id:
            await ctx.reply("You cannot ban yourself!")
        
        else:
            try:
                await member.ban(reason=reason)
                await ctx.reply(embed = BanA)
            except:
                await ctx.reply(embed = BanB)

@bot.command()
@has_permissions(ban_members = True)
async def unban(ctx, member : int = None):
    if member == None:

        Unban = discord.Embed(
            title = "Unban",
            description = "Unbans the user by their discord user ID \n Example: `'unban 705435835306213418 Very cool`",
            colour = discord.Colour.light_gray())

        await ctx.reply(embed = Unban)

    else: 

        UnbanA = discord.Embed(
            title = ":white_check_mark: Unban Successful :white_check_mark:",
            description = (f"Successfully unbanned <@{member}>"),
            colour = discord.Colour.green())

        UnbanB = discord.Embed(
            title = ":warning: Error :warning:",
            description = (f"Could not unban <@{member}> because they are not banned"),
            colour = discord.Colour.dark_orange())

        for ban in await ctx.guild.bans():
            if ban.user.id == int(member):
                await ctx.guild.unban(ban.user)
                return await ctx.reply(embed = UnbanA)

        await ctx.reply(embed = UnbanB)

#Moderation commands above

#Economy commands below

users = {}
fish_cooldown = {}
hunt_cooldown = {}
hourly_cooldown = {}

hunt_items = {
    "skunk": {"chance": 20, "price": 50},
    "pig": {"chance": 15, "price": 100},
    "cow": {"chance": 10, "price": 200},
    "deer": {"chance": 7, "price": 300},
    "bear": {"chance": 5, "price": 400},
    "junk": {"chance": 2, "price": 25},
    "treasure": {"chance": 0.5, "price": 10000}}

fish_items = {
    "common fish": {"chance": 45, "price": 10},
    "uncommon fish": {"chance": 30, "price": 20},
    "rare fish": {"chance": 15, "price": 50},
    "epic fish": {"chance": 7, "price": 200},
    "legendary fish": {"chance": 1, "price": 1000},
    "junk": {"chance": 0.9, "price": 25},
    "treasure": {"chance": 0.1, "price": 10000},
    "seaweed": {"chance": 1, "price": 25}}

sell_prices = {
    "common fish": 5,
    "uncommon fish": 10,
    "rare fish": 25,
    "epic fish": 100,
    "legendary fish": 500,
    "junk": 15,
    "treasure": 10000,
    "seaweed": 15,
    "skunk": 5,
    "pig": 10,
    "cow": 25,
    "deer": 150,
    "bear": 200}

try:
    with open('data/users.json', 'r') as f:
        users = json.load(f)
except:
    print('Could not load data')

def save_data():
    with open('data/users.json', 'w') as f:
        json.dump(users, f, indent=4)

@bot.command(name='start')
async def _start(ctx):
    user_id = str(ctx.author.id)
    try:
        with open("data/users.json", "r") as f:
            data = json.load(f)

    except FileNotFoundError:
        data = {}

    CommandExecuted = discord.Embed(
            title = "Command Already Executed",
            description = "You have already executed this command.",
            colour = discord.Colour.red())

    if user_id in data:
        await ctx.reply(embed = CommandExecuted)
        return
    data[user_id] = {"inventory": {}, "balance": 0}
    with open("data/users.json", "w") as f:
        json.dump(data, f, indent=4)

    CommandSuccess = discord.Embed(
        title = "Command Executed",
        description = "Success: You can now use Tester69 bot",
        colour = discord.Colour.green())
    await ctx.reply(embed = CommandSuccess)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        user_id = str(ctx.author.id)

        Error = discord.Embed(
            title = "ERROR",
            description = "users.json not found",
            colour = discord.Colour.red())

        try:
            with open("data/users.json", "r") as f:
                data = json.load(f)

        except FileNotFoundError:
            await ctx.reply(embed = Error)
            return

        if user_id not in data:
            await ctx.reply(embed = Start)
            return
    raise error

@bot.command()
async def balance(ctx):
    user_id = str(ctx.author.id)

    try:
        with open("data/users.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        await ctx.reply("Error: users.json not found.")
        return
    if user_id not in data:
        await ctx.reply(embed = Start)
        return

    Balance = discord.Embed(
        title = "Balance",
        description = (f'Your balance is {users[user_id]["balance"]} coins'),
        colour = discord.Colour.green())

    Balance2 = discord.Embed(
        title = "Balance",
        description = (f'Your balance is {users[user_id]["balance"]} coins'),
        colour = discord.Colour.green())

    if user_id in users:
        await ctx.reply(embed = Balance)
    else:
        users[user_id] = {"balance": 0}
        save_data()
        await ctx.reply(embed = Balance2)

@bot.command()
async def add(ctx, amount: int = None):
    user_id = str(ctx.author.id)

    try:
        with open("data/users.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        await ctx.reply("Error: users.json not found.")
        return
    if user_id not in data:
        await ctx.reply(embed = Start)
        return

    NoNumber = discord.Embed(
        title = "No Value",
        description = "You have to add a number between 1 - infinity, for example `'add 1000`",
        colour = discord.Colour.orange())

    if amount is None:
        await ctx.reply(embed = NoNumber)
        return

    add = discord.Embed(
        title = "Added Coins",
        description = (f'Added {amount} coins to your balance. Your new balance is {users[user_id]["balance"]}'),
        colour = discord.Colour.green())

    add2 = discord.Embed(
        title = "Added Coins",
        description = (f'Added {amount} coins to your balance. Your new balance is {users[user_id]["balance"]}'),
        colour = discord.Colour.green())

    if user_id in users:
        users[user_id]["balance"] += amount
        save_data()
        await ctx.reply(embed = add)
    else:
        users[user_id] = {"balance": amount}
        save_data()
        await ctx.reply(embed = add2)

@bot.command()
async def subtract(ctx, amount: int = None):
    user_id = str(ctx.author.id)

    try:
        with open("data/users.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        await ctx.reply("Error: users.json not found.")
        return
    if user_id not in data:
        await ctx.reply(embed = Start)
        return

    NoNumber = discord.Embed(
        title = "No Value",
        description = "You have to add a number between 1 - infinity, for example `'subtract 1000`",
        colour = discord.Colour.orange())

    if amount is None:
        await ctx.reply(embed = NoNumber)
        return

    SubtractFail = discord.Embed(
        title = "Coin Subtraction Failed",
        description = (f'You do not have enough coins. Your new balance is {users[user_id]["balance"]}'),
        colour = discord.Colour.red())

    SubtractSuccess = discord.Embed(
        title = "Coin Subtraction Succeeded",
        description = (f'Subtracted {amount} from your balance. Your new balance is {users[user_id]["balance"]}'),
        colour = discord.Color.green())
    
    NoCoins = discord.Embed(
        title = "No Coins",
        description = "You do not have any coins to subtract",
        colour = discord.Color.orange())

    if user_id in users:
        if users[user_id]["balance"] - amount < 0:
            await ctx.reply(embed = SubtractFail)
        else:
            users[user_id]["balance"] -= amount
            save_data()
            await ctx.reply(embed = SubtractSuccess)
    else:
        await ctx.reply(embed = NoCoins)

@bot.command()
async def hunt(ctx):
    user_id = str(ctx.author.id)
    if user_id in whitelist:
        pass
    elif user_id in hunt_cooldown and hunt_cooldown[user_id] > datetime.now():
        remaining = hunt_cooldown[user_id] - datetime.now()

        Cooldown = discord.Embed(
        title = "Cooldown",
        description = (f"You're still on cooldown for {remaining.seconds // 60} minutes and {remaining.seconds % 60} seconds."),
        colour = discord.Colour.orange())

        await ctx.reply(embed = Cooldown)
        return

    with open("data/users.json", "r") as f:
        data = json.load(f)
    if user_id not in data:
        await ctx.reply(embed = Start)
        return
    if 'inventory' not in data[user_id]:
        data[user_id]['inventory'] = {}
    item_name, item_data = random_choice_from_dict(hunt_items)
    if item_name not in data[user_id]['inventory']:
        data[user_id]['inventory'][item_name] = 0
    data[user_id]['inventory'][item_name] += 1
    with open("data/users.json", "w") as f:
        json.dump(data, f, indent=4)

    CaughtAnimal = discord.Embed(
        title = "Item Caught",
        description = (f'You hunted down a {item_name}!'),
        colour = discord.Colour.green())
        
    await ctx.reply(embed = CaughtAnimal)
    print(f'{user_id} caught a {item_name}')

    hunt_cooldown[user_id] = datetime.now() + timedelta(minutes=10)

def random_choice_from_dict(d):
    total_chance = sum(item['chance'] for item in d.values())
    rand = random.uniform(0, total_chance)
    for item_name, item_data in d.items():
        if rand < item_data['chance']:
            return item_name, item_data
        rand -= item_data['chance']

@bot.command()
async def fish(ctx):
    user_id = str(ctx.author.id)
    if user_id in whitelist:
        pass
    elif user_id in fish_cooldown and fish_cooldown[user_id] > datetime.now():
        remaining = fish_cooldown[user_id] - datetime.now()

        Cooldown = discord.Embed(
            title = "Cooldown",
            description = (f"You're still on cooldown for {remaining.seconds // 60} minutes and {remaining.seconds % 60} seconds."),
            colour = discord.Colour.orange())

        await ctx.reply(embed = Cooldown)
        return

    with open("data/users.json", "r") as f:
        data = json.load(f)
    if user_id not in data:
        await ctx.reply(embed = Start)
        return
    if 'inventory' not in data[user_id]:
        data[user_id]['inventory'] = {}
    item_name, item_data = random_choice_from_dict(fish_items)
    if item_name not in data[user_id]['inventory']:
        data[user_id]['inventory'][item_name] = 0
    data[user_id]['inventory'][item_name] += 1
    with open("data/users.json", "w") as f:
        json.dump(data, f, indent=4)

    CaughtFish = discord.Embed(
        title = "Item Caught",
        description = (f'You caught a {item_name}!'),
        colour = discord.Colour.green())

    await ctx.reply(embed = CaughtFish)
    print(f'{user_id} caught a {item_name}')

    fish_cooldown[user_id] = datetime.now() + timedelta(minutes=10)

def random_choice_from_dict(d):
    total_chance = sum(item['chance'] for item in d.values())
    rand = random.uniform(0, total_chance)
    for item_name, item_data in d.items():
        if rand < item_data['chance']:
            return item_name, item_data
        rand -= item_data['chance']

@bot.command()
async def sell(ctx, item: str):
    user_id = str(ctx.author.id)
    item = item.lower()
    with open("data/users.json", "r") as f:
        data = json.load(f)
    if user_id not in data:
        await ctx.reply(embed = Start)
        return

    NoItem = discord.Embed(
        title = "No Item",
        description = "You don't have any of that item.",
        colour = discord.Colour.orange())

    if 'inventory' not in data[user_id] or item not in data[user_id]['inventory']:
        await ctx.reply(embed = NoItem)
        return

    NoItem2 = discord.Embed(
        title = "No Item",
        description = "You don't have any of that item.",
        colour = discord.Colour.orange())

    if data[user_id]['inventory'][item] <= 0:
        await ctx.reply(embed = NoItem2)
        return

    NoCanBuy = discord.Embed(
        title = "Can't Buy",
        description = "I can't buy that.",
        colour = discord.Colour.red())

    if item not in sell_prices:
        await ctx.reply(embed = NoCanBuy)
        return

    SoldItem = discord.Embed(
        title = "Item Sold",
        description = (f'You sold a {item} for {price} coins!'),
        colour = discord.Colour.green())

    price = sell_prices[item]
    data[user_id]['balance'] += price
    data[user_id]['inventory'][item] -= 1
    with open("data/users.json", "w") as f:
        json.dump(data, f, indent=4)
    await ctx.reply(embed = SoldItem)
    print(f'{user_id} sold a {item} for {price} coins')

@bot.command()
async def hourly(ctx):
    user_id = str(ctx.author.id)
    if user_id in whitelist:
        pass
    elif user_id in hourly_cooldown and hourly_cooldown[user_id] > datetime.now():
        remaining = hourly_cooldown[user_id] - datetime.now()
        minutes, seconds = divmod(remaining.seconds, 60)
        hours, minutes = divmod(minutes, 60)

        Cooldown = discord.Embed(
            title = "Cooldown",
            description = (f"You're still on cooldown for {remaining.seconds // 60} minutes and {remaining.seconds % 60} seconds."),
            colour = discord.Colour.orange())

        await ctx.reply(embed = Cooldown)
        return

    with open("data/users.json", "r") as f:
        data = json.load(f)
    if user_id not in data:
        await ctx.reply(embed = Start)
        return
    if 'balance' not in data[user_id]:
        data[user_id]['balance'] = 0
    data[user_id]['balance'] += 10
    with open("data/users.json", "w") as f:
        json.dump(data, f, indent=4)

    HourlyPay = discord.Embed(
        title = "Hourly Pay",
        description = "You received 10 coins!",
        colour = discord.Colour.green())

    await ctx.send(embed = HourlyPay)

    hourly_cooldown[user_id] = datetime.now() + timedelta(hours=1)

@bot.command()
async def inventory(ctx):
    user_id = str(ctx.author.id)

    try:
        with open("data/users.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        await ctx.reply("Error: users.json not found.")
        return
    if user_id not in data:
        await ctx.reply(embed = Start)
        return

    NoInventory = discord.Embed(
        title = "No Inventory",
        description = "You do not have an inventory.",
        colour = discord.Colour.orange())
    
    InventoryEmpty = discord.Embed(
        title = "Inventory Empty",
        description = "Your inventory is empty",
        colour = discord.Colour.orange())

    try:
        with open(f"data/users.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        await ctx.reply(embed = NoInventory)
        return
    user_data = data.get(user_id, {})
    inventory = user_data.get("inventory", {})
    if not inventory:
        await ctx.reply(embed = InventoryEmpty)
    else:
        message = "```Inventory:\n"
        for item, count in inventory.items():
            message += f"{item}: {count}\n"
        message += "```"

        Inventory = discord.Embed(
            title = "Inventory",
            description = (f'{message}'),
            colour = discord.Colour.green())
    
        await ctx.reply(embed = Inventory)


@bot.command()
async def devskip(ctx, user: discord.User):
    if str(ctx.message.author.id) not in whitelist:

        NoPermission = discord.Embed(
            title = "No Permission",
            description = "You do not have permission to use this command.",
            colour = discord.Colour.orange())

        await ctx.reply(embed = NoPermission)
        return

    FishSkip = discord.Embed(
        title = "Cooldown Skipped",
        description = (f'{user.name}\'s fishing cooldown has been skipped'),
        colour = discord.Color.green())

    HuntSkip = discord.Embed(
        title = "Cooldown Skipped",
        description = (f'{user.name}\'s hunt command cooldown has been skipped'),
        colour = discord.Colour.green())

    HourlySkip = discord.Embed(
        title = "Cooldown Skipped",
        description = (f'{user.name}\'s hourly command cooldown has been skipped'),
        colour = discord.Color.green())

    NoCooldown = discord.Embed(
        title = "No Cooldowns",
        description = (f'{user.name} doesn\'t have any active cooldowns'),
        colour = discord.Color.orange())

    user_id = str(user.id)
    flag = False
    if user_id in fish_cooldown:
        del fish_cooldown[user_id]
        await ctx.reply(embed = FishSkip)
        flag = True
    if user_id in hourly_cooldown:
        del hourly_cooldown[user_id]
        await ctx.reply(embed = HourlySkip)
        flag = True
    if user_id in hunt_cooldown:
        del hunt_cooldown[user_id]
        await ctx.reply(embed = HuntSkip)
        flag = True
    if not flag:
        await ctx.reply(embed = NoCooldown)

@bot.command(name='gamble')
async def _gamble(ctx, bet:int = None):
    user_id = str(ctx.author.id)

    try:
        with open("data/users.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        await ctx.reply("Error: users.json not found.")
        return
    if user_id not in data:
        await ctx.reply(embed = Start)
        return

    NotGoodBet = discord.Embed(
        title = "Bet Failed",
        description = "You have to add a bet between 0 and 10000000, for example `'gamble 10`",
        colour = discord.Colour.orange())

    if bet is None or bet < 0 or bet > 10000000:
        await ctx.reply(embed = NotGoodBet)
        return

    TooHighBet = discord.Embed(
        title = "Too High Bet",
        description = (f'You cannot bet more than 10 million coins'),
        colour = discord.Colour.orange())

    NoFunds = discord.Embed(
        title = "No Coins To Gamble",
        description = (f'You do not have enough funds to gamble. Your balance is {users[user_id]["balance"]}'),
        colour = discord.Colour.orange())

    NoFunds2 = discord.Embed(
        title = "No Coins To Gamble",
        description = (f'You do not have enough funds to gamble. Your balance is {users[user_id]["balance"]}'),
        colour = discord.Colour.orange())

    if user_id in users:
        if bet > 10000000:
            await ctx.reply(embed = TooHighBet)
            return
        if bet > users[user_id]['balance']:
            await ctx.reply(embed = NoFunds)
            return
        users[user_id]["balance"] -= bet
        save_data()
        win = random.choices([True, False], [45, 55])[0]
        if win:
            multipliers = [0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2]
            chances = [13,12,11,10,10,9,8,7,6,5,4,3,2]
            multiplier = random.choices(multipliers, chances)[0]
            winnings = int(bet*multiplier)
            users[user_id]["balance"] += winnings
            save_data()

            BetWinnings = discord.Embed(
                title = "Bet Results",
                description = (f'Congratulations! You won {winnings - bet} and your new balance is {users[user_id]["balance"]}'),
                colour = discord.Colour.green())

            print(f'{ctx.message.author} won at a {multiplier}x multiplier with a {chances[multipliers.index(multiplier)]}% chance and total winnings of {winnings}')

            await ctx.reply(embed = BetWinnings)
        else:

            BetLoss = discord.Embed(
                title = "Bet Results",
                description = (f'Sorry, you lost {bet}. Your new balance is {users[user_id]["balance"]}'),
                colour = discord.Colour.red())

            await ctx.reply(embed = BetLoss)
    else:
        await ctx.reply(embed = NoFunds2)

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

bot.run("<Your bot token here>")