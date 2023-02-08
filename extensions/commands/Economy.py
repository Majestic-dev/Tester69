from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
from datetime import datetime
import discord
import json
import random

whitelist = [705435835306213418]
owners = [705435835306213418]

Start = discord.Embed(
    title="ERROR",
    description="You need to execute the `/start` command before executing any other commands",
    colour=discord.Colour.dark_orange(),)

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
    "treasure": {"chance": 0.5, "price": 10000},}

fish_items = {
    "common fish": {"chance": 45, "price": 10},
    "uncommon fish": {"chance": 30, "price": 20},
    "rare fish": {"chance": 15, "price": 50},
    "epic fish": {"chance": 7, "price": 200},
    "legendary fish": {"chance": 1, "price": 1000},
    "junk": {"chance": 0.9, "price": 25},
    "treasure": {"chance": 0.1, "price": 10000},
    "seaweed": {"chance": 1, "price": 25},}

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
    "bear": 200,}


def load_data():
    try:
        with open("data/users.json", "r") as f:
            return json.load(f)
    except:
        print("Could not load data")


def save_data(data):
    with open("data/users.json", "w") as f:
        json.dump(data, f, indent=4)


def random_choice_from_dict(d):
    total_chance = sum(item["chance"] for item in d.values())
    rand = random.uniform(0, total_chance)
    for item_name, item_data in d.items():
        if rand < item_data["chance"]:
            return item_name, item_data
        rand -= item_data["chance"]


class Economy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="start", description="Start your tester69 journey!")
    async def _start(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        try:
            with open("data/users.json", "r") as f:
                data = json.load(f)

        except FileNotFoundError:
            data = {}

        CommandExecuted = discord.Embed(
            title="Command Already Executed",
            description="You have already executed this command.",
            colour=discord.Colour.red(),
        )

        if user_id in data:
            await interaction.response.send_message(embed=CommandExecuted)
            return
        data[user_id] = {"inventory": {}, "balance": 0}
        with open("data/users.json", "w") as f:
            json.dump(data, f, indent=4)

        CommandSuccess = discord.Embed(
            title="Command Executed",
            description="Success: You can now use Tester69 bot",
            colour=discord.Colour.green(),
        )
        await interaction.response.send_message(embed=CommandSuccess)

    @app_commands.command(name="balance", description="Check your coin balance")
    async def balance(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)

        try:
            with open("data/users.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            await interaction.response.send_message("Error: users.json not found.")
            return
        if user_id not in data:
            await interaction.response.send_message(embed=Start)
            return

        Balance = discord.Embed(
            title="Balance",
            description=(f'Your balance is {data[user_id]["balance"]} coins'),
            colour=discord.Colour.green(),
        )

        Balance2 = discord.Embed(
            title="Balance",
            description=(f'Your balance is {data[user_id]["balance"]} coins'),
            colour=discord.Colour.green(),
        )

        if user_id in data:
            await interaction.response.send_message(embed=Balance)
        else:
            data[user_id] = {"balance": 0}
            save_data(data)
            await interaction.response.send_message(embed=Balance2)

    @app_commands.command(
        name="add", description="Add set amount of coins to your balance"
    )
    @commands.is_owner()
    async def add(
        self,
        interaction: discord.Interaction,
        member: discord.Member = None,
        amount: int = None,
    ):
        user_id = str(interaction.user.id)

        data = load_data()
        if user_id not in data:
            await interaction.response.send_message(embed=Start)
            return

        NoNumber = discord.Embed(
            title="No Value",
            description="You have to add a number between 1 - infinity, for example `'add 1000`",
            colour=discord.Colour.orange(),
        )

        if amount is None:
            await interaction.response.send_message(embed=NoNumber)
            return

        if user_id in data:
            data[user_id]["balance"] += amount
            save_data(data)

            add = discord.Embed(
                title="Added Coins",
                description=(
                    f'Added {amount} coins to your balance. Your new balance is {data[user_id]["balance"]}'
                ),
                colour=discord.Colour.green(),
            )

            await interaction.response.send_message(embed=add)
        else:
            data[user_id] = {"balance": amount}
            save_data(data)

            add2 = discord.Embed(
                title="Added Coins",
                description=(
                    f'Added {amount} coins to your balance. Your new balance is {data[user_id]["balance"]}'
                ),
                colour=discord.Colour.green(),
            )

            await interaction.response.send_message(embed=add2)

    @app_commands.command(
        name="subtract", description="Subtract set amount of coins from your balance"
    )
    @commands.is_owner()
    async def subtract(
        self,
        interaction: discord.Interaction,
        member: discord.Member = None,
        amount: int = None,
    ):
        user_id = str(interaction.user.id)

        try:
            with open("data/users.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            await interaction.response.send_message("Error: users.json not found.")
            return
        if user_id not in data:
            await interaction.response.send_message(embed=Start)
            return

        NoNumber = discord.Embed(
            title="No Value",
            description="You have to add a number between 1 - infinity, for example `'subtract 1000`",
            colour=discord.Colour.orange(),
        )

        if amount is None:
            await interaction.response.send_message(embed=NoNumber)
            return

        SubtractFail = discord.Embed(
            title="Coin Subtraction Failed",
            description=(
                f'You do not have enough coins. Your new balance is {data[user_id]["balance"]}'
            ),
            colour=discord.Colour.red(),
        )

        NoCoins = discord.Embed(
            title="No Coins",
            description="You do not have any coins to subtract",
            colour=discord.Color.orange(),
        )

        if user_id in data:
            if data[user_id]["balance"] - amount < 0:
                await interaction.response.send_message(embed=SubtractFail)
            else:
                data[user_id]["balance"] -= amount
                save_data(data)

                SubtractSuccess = discord.Embed(
                    title="Coin Subtraction Succeeded",
                    description=(
                        f'Subtracted {amount} from your balance. Your new balance is {data[user_id]["balance"]}'
                    ),
                    colour=discord.Color.green(),
                )

                await interaction.response.send_message(embed=SubtractSuccess)
        else:
            await interaction.response.send_message(embed=NoCoins)

    @app_commands.command(name="hunt", description="Hunt for some loot")
    async def hunt(self, interaction: discord.Interaction):

        user_id = str(interaction.user.id)
        if user_id in whitelist:
            pass
        elif user_id in hunt_cooldown and hunt_cooldown[user_id] > datetime.now():
            remaining = hunt_cooldown[user_id] - datetime.now()

            Cooldown = discord.Embed(
                title="Cooldown",
                description=(
                    f"You're still on cooldown for {remaining.seconds // 60} minutes and {remaining.seconds % 60} seconds."
                ),
                colour=discord.Colour.orange(),
            )

            await interaction.response.send_message(embed=Cooldown)
            return

        with open("data/users.json", "r") as f:
            data = json.load(f)
        if user_id not in data:
            await interaction.response.send_message(embed=Start)
            return
        if "inventory" not in data[user_id]:
            data[user_id]["inventory"] = {}
        item_name, item_data = random_choice_from_dict(hunt_items)
        if item_name not in data[user_id]["inventory"]:
            data[user_id]["inventory"][item_name] = 0
        data[user_id]["inventory"][item_name] += 1
        with open("data/users.json", "w") as f:
            json.dump(data, f, indent=4)

        CaughtAnimal = discord.Embed(
            title="Item Caught",
            description=(f"You hunted down a {item_name}!"),
            colour=discord.Colour.green(),
        )

        await interaction.response.send_message(embed=CaughtAnimal)
        print(f"{user_id} caught a {item_name}")

        hunt_cooldown[user_id] = datetime.now() + timedelta(minutes=10)

    def random_choice_from_dict(d):
        total_chance = sum(item["chance"] for item in d.values())
        rand = random.uniform(0, total_chance)
        for item_name, item_data in d.items():
            if rand < item_data["chance"]:
                return item_name, item_data
            rand -= item_data["chance"]

    @app_commands.command(name="fish", description="Fish for some loot")
    async def fish(self, interaction: discord.Interaction):

        user_id = str(interaction.user.id)
        if user_id in whitelist:
            pass
        elif user_id in fish_cooldown and fish_cooldown[user_id] > datetime.now():
            remaining = fish_cooldown[user_id] - datetime.now()

            Cooldown = discord.Embed(
                title="Cooldown",
                description=(
                    f"You're still on cooldown for {remaining.seconds // 60} minutes and {remaining.seconds % 60} seconds."
                ),
                colour=discord.Colour.orange(),
            )

            await interaction.response.send_message(embed=Cooldown)
            return

        with open("data/users.json", "r") as f:
            data = json.load(f)
        if user_id not in data:
            await interaction.response.send_message(embed=Start)
            return
        if "inventory" not in data[user_id]:
            data[user_id]["inventory"] = {}
        item_name, item_data = random_choice_from_dict(fish_items)
        if item_name not in data[user_id]["inventory"]:
            data[user_id]["inventory"][item_name] = 0
        data[user_id]["inventory"][item_name] += 1
        with open("data/users.json", "w") as f:
            json.dump(data, f, indent=4)

        CaughtFish = discord.Embed(
            title="Item Caught",
            description=(f"You caught a {item_name}!"),
            colour=discord.Colour.green(),
        )

        await interaction.response.send_message(embed=CaughtFish)
        print(f"{user_id} caught a {item_name}")

        fish_cooldown[user_id] = datetime.now() + timedelta(minutes=10)

    def random_choice_from_dict(d):
        total_chance = sum(item["chance"] for item in d.values())
        rand = random.uniform(0, total_chance)
        for item_name, item_data in d.items():
            if rand < item_data["chance"]:
                return item_name, item_data
            rand -= item_data["chance"]

    async def item_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        with open("data/users.json", "r") as f:
            data = json.load(f)

        if str(interaction.user.id) not in data:
            return

        user_data = data[str(interaction.user.id)]

        if "inventory" not in user_data:
            return

        items_in_inventory = list(user_data["inventory"].keys())

        return [
            app_commands.Choice(name=item, value=item)
            for item in items_in_inventory
            if item.lower().startswith(current.lower())
            or len(current) < 2
            and user_data["inventory"][item] > 0
        ]

    @app_commands.command(name="sell", description="Sell your loot for coins")
    @app_commands.autocomplete(item=item_autocomplete)
    async def sell(self, interaction: discord.Interaction, item: str):
        user_id = str(interaction.user.id)
        item = item.lower()
        with open("data/users.json", "r") as f:
            data = json.load(f)
        if user_id not in data:
            await interaction.response.send_message(embed=Start)
            return

        NoItem = discord.Embed(
            title="No Item",
            description="You don't have any of that item.",
            colour=discord.Colour.orange(),
        )

        if "inventory" not in data[user_id] or item not in data[user_id]["inventory"]:
            await interaction.response.send_message(embed=NoItem)
            return

        NoItem2 = discord.Embed(
            title="No Item",
            description="You don't have any of that item.",
            colour=discord.Colour.orange(),
        )

        if data[user_id]["inventory"][item] <= 0:
            await interaction.response.send_message(embed=NoItem2)
            return

        NoCanBuy = discord.Embed(
            title="Can't Sell",
            description="I can't sell that item, because it doesn't exist",
            colour=discord.Colour.red(),
        )

        if item not in sell_prices:
            await interaction.response.send_message(embed=NoCanBuy)
            return

        price = sell_prices[item]
        data[user_id]["balance"] += price
        data[user_id]["inventory"][item] -= 1
        with open("data/users.json", "w") as f:
            json.dump(data, f, indent=4)
        print(f"{user_id} sold a {item} for {price} coins")

        SoldItem = discord.Embed(
            title="Item Sold",
            description=(f"You sold a {item} for {price} coins!"),
            colour=discord.Colour.green(),
        )

        await interaction.response.send_message(embed=SoldItem)

    @app_commands.command(
        name="hourly", description="Gain 10 coins every time you use this command"
    )
    async def hourly(self, interaction: discord.Interaction):

        user_id = str(interaction.user.id)
        if user_id in whitelist:
            pass
        elif user_id in hourly_cooldown and hourly_cooldown[user_id] > datetime.now():
            remaining = hourly_cooldown[user_id] - datetime.now()
            minutes, seconds = divmod(remaining.seconds, 60)
            hours, minutes = divmod(minutes, 60)

            Cooldown = discord.Embed(
                title="Cooldown",
                description=(
                    f"You're still on cooldown for {remaining.seconds // 60} minutes and {remaining.seconds % 60} seconds."
                ),
                colour=discord.Colour.orange(),
            )

            await interaction.response.send_message(embed=Cooldown)
            return

        with open("data/users.json", "r") as f:
            data = json.load(f)
        if user_id not in data:
            await interaction.response.send_message(embed=Start)
            return
        if "balance" not in data[user_id]:
            data[user_id]["balance"] = 0
        data[user_id]["balance"] += 10
        with open("data/users.json", "w") as f:
            json.dump(data, f, indent=4)

        HourlyPay = discord.Embed(
            title="Hourly Pay",
            description="You received 10 coins!",
            colour=discord.Colour.green(),
        )

        await interaction.response.send_message(embed=HourlyPay)

        hourly_cooldown[user_id] = datetime.now() + timedelta(hours=1)

    @app_commands.command(name="inventory", description="See your inventory")
    async def inventory(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)

        try:
            with open("data/users.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            await interaction.response.send_message("Error: users.json not found.")
            return
        if user_id not in data:
            await interaction.response.send_message(embed=Start)
            return

        NoInventory = discord.Embed(
            title="No Inventory",
            description="You do not have an inventory.",
            colour=discord.Colour.orange(),
        )

        InventoryEmpty = discord.Embed(
            title="Inventory Empty",
            description="Your inventory is empty",
            colour=discord.Colour.orange(),
        )

        try:
            with open(f"data/users.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            await interaction.response.send_message(embed=NoInventory)
            return
        user_data = data.get(user_id, {})
        inventory = user_data.get("inventory", {})
        if not inventory:
            await interaction.response.send_message(embed=InventoryEmpty)
        else:
            message = "```Inventory:\n"
            for item, count in inventory.items():
                message += f"{item}: {count}\n"
            message += "```"

            Inventory = discord.Embed(
                title="Inventory",
                description=(f"{message}"),
                colour=discord.Colour.green(),
            )

            await interaction.response.send_message(embed=Inventory)

    @app_commands.command(
        name="devskip", description="Skip all cooldowns of the mentioned user"
    )
    @commands.is_owner()
    async def devskip(self, interaction: discord.Interaction, user: discord.User):

        Skip = discord.Embed(
            title="Cooldown Skipped",
            description=(f"{user.name}'s fishing cooldown has been skipped"),
            colour=discord.Color.green(),
        )

        Skip2 = discord.Embed(
            title="Cooldowns Skipped",
            description=(
                f"{user.name}'s fishing and hunting cooldowns have been skipped"
            ),
            colour=discord.Colour.green(),
        )

        Skip3 = discord.Embed(
            title="Cooldowns Skipped",
            description=(
                f"{user.name}'s fishing and hourly cooldowns have been skipped"
            ),
            colour=discord.Colour.green(),
        )

        Skip4 = discord.Embed(
            title="Cooldown Skipped",
            description=(f"{user.name}'s hunting cooldown has been skipped"),
            colour=discord.Colour.green(),
        )

        Skip5 = discord.Embed(
            title="Cooldowns Skipped",
            description=(
                f"{user.name}'s hunting and hourly cooldowns have been skipped"
            ),
            colour=discord.Colour.green(),
        )

        Skip6 = discord.Embed(
            title="Cooldowns Skipped",
            description=(f"all of {user.name}'s cooldowns have been skipped"),
            colour=discord.Color.green(),
        )

        NoCooldown = discord.Embed(
            title="No Cooldowns",
            description=(f"{user.name} doesn't have any active cooldowns"),
            colour=discord.Color.orange(),
        )

        user_id = str(user.id)
        flag = False
        if user_id in fish_cooldown and hunt_cooldown and hourly_cooldown:
            del fish_cooldown[user_id]
            del hunt_cooldown[user_id]
            del hourly_cooldown[user_id]
            await interaction.response.send_message(embed=Skip3)
            flag = True
        if user_id in fish_cooldown and hunt_cooldown:
            del hunt_cooldown[user_id]
            del fish_cooldown[user_id]
            await interaction.response.send_message(embed=Skip2)
            flag = True
        if user_id in fish_cooldown and hourly_cooldown:
            del fish_cooldown[user_id]
            del hourly_cooldown[user_id]
            await interaction.response.send_message(embed=Skip3)
            flag = True
        if user_id in hunt_cooldown and hourly_cooldown:
            del hunt_cooldown[user_id]
            del hourly_cooldown[user_id]
            await interaction.response.send_message(embed=Skip5)
            flag = True
        if user_id in fish_cooldown:
            del fish_cooldown[user_id]
            await interaction.response.send_message(embed=Skip)
            flag = True
        if user_id in hunt_cooldown:
            del hunt_cooldown[user_id]
            await interaction.response.send_message(embed=Skip4)
            flag = True
        if not flag:
            await interaction.response.send_message(embed=NoCooldown)


async def setup(bot: commands.Bot):
    await bot.add_cog(Economy(bot))
