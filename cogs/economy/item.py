import json
import string

import discord
from discord import app_commands
from discord.ext import commands

from utils import data_manager, paginator, UserData


class item(commands.GroupCog):
    def __init__(self, bot):
        self.bot = bot

    async def item_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        user_data: UserData = await data_manager.get_user_data(interaction.user.id)
        items_in_inventory = json.loads(user_data["inventory"]).keys()

        item_list = [
            app_commands.Choice(name=item, value=item)
            for item in items_in_inventory
            if item.lower().startswith(current.lower())
            or len(current) < 1
            and user_data["inventory"][item] > 0
        ]

        return item_list[0:25]

    @app_commands.command(name="sell", description="Sell your loot for 🪙")
    @app_commands.autocomplete(item=item_autocomplete)
    @app_commands.checks.cooldown(1, 15, key=lambda i: (i.user.id))
    @app_commands.describe(
        item="The item you want to sell",
        amount="The amount of the item you want to sell (defaults to 1)",
    )
    async def sell(self, interaction: discord.Interaction, item: str, amount: int = 1):
        if amount <= 0:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You can't sell 0 or a negative amount of items",
                    colour=discord.Colour.red(),
                )
            )

        items = data_manager.get("economy", "items")
        if not items:
            print("where are the items gang")

        user_data: UserData = await data_manager.get_user_data(interaction.user.id)

        if user_data["inventory"] is not None and json.loads(user_data["inventory"]):
            user_inv = json.loads(user_data["inventory"])
        else:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You don't have any items in your inventory",
                    colour=discord.Colour.orange(),
                )
            )

        item1 = items.get(item.lower(), None)

        if item1:
            if (
                user_data["inventory"] is None
                or item.lower() not in user_data["inventory"]
            ):
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        description="<:white_cross:1096791282023669860> You don't have any of that item",
                        colour=discord.Colour.orange(),
                    )
                )

            if int(user_inv[item]) < amount:
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        description="<:white_cross:1096791282023669860> You don't have enough of that item",
                        colour=discord.Colour.orange(),
                    )
                )

            price = item1["sell price"]
            await data_manager.edit_user_data(
                interaction.user.id,
                "balance",
                user_data["balance"] + (int(amount) * price),
            )
            await data_manager.edit_user_inventory(
                interaction.user.id, item, -int(amount)
            )

            await interaction.response.send_message(
                embed=discord.Embed(
                    description=f"<:white_checkmark:1096793014287995061> Sold {amount} **{item1['emoji']} {item1['name']}** for **{(int(amount) * price)} 🪙**",
                    colour=discord.Colour.green(),
                )
            )
        else:
            await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> That item doesn't exist",
                    colour=discord.Colour.red(),
                )
            )

    @app_commands.command(name="shop", description="View the shop to buy various items")
    @app_commands.checks.cooldown(1, 15, key=lambda i: (i.user.id))
    async def shop(self, interaction: discord.Interaction):
        user_data: UserData = await data_manager.get_user_data(interaction.user.id)

        embeds = []

        cur_embed = discord.Embed(
            title="Shop", colour=discord.Colour.from_rgb(43, 45, 49)
        )

        for item in data_manager.get("economy", "items"):
            if len(cur_embed.fields) >= 8:
                embeds.append(cur_embed)

                cur_embed = discord.Embed(
                    title="Shop",
                    colour=discord.Colour.green(),
                )

            items = data_manager.get("economy", "items")

            price = items[item]["buy price"]
            description = items[item]["description"]
            emoji = items[item]["emoji"]

            if price != 0:
                if user_data["inventory"] is not None:
                    if item.lower() in user_data["inventory"]:
                        cur_embed.add_field(
                            name=f"{emoji} **{item.title()}**"
                            + f" ({json.loads(user_data['inventory'])[item.lower()]}) - {price} 🪙",
                            value=f"{description}",
                            inline=False,
                        )
                else:
                    cur_embed.add_field(
                        name=f"{emoji} **{item.title()}**" + f" - {price} 🪙",
                        value=f"{description}",
                        inline=False,
                    )
            else:
                pass

        embeds.append(cur_embed)

        await paginator.Simple().paginate(interaction, embeds)

    async def item_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        shop_items = data_manager.get("economy", "shop items").keys()

        return [
            app_commands.Choice(name=item, value=item)
            for item in shop_items
            if item.lower().startswith(current.lower()) or len(current) < 1
        ]

    @app_commands.command(name="buy", description="Buy an item")
    @app_commands.autocomplete(item=item_autocomplete)
    @app_commands.checks.cooldown(1, 15, key=lambda i: (i.user.id))
    @app_commands.describe(
        item="The item you want to buy",
        amount="The amount of the item you want to buy (defaults to 1)",
    )
    async def buy_item(
        self, interaction: discord.Interaction, item: str, amount: int = 1
    ):
        if amount <= 0:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You can't buy 0 or a negative amount of items",
                    colour=discord.Colour.red(),
                )
            )

        shop_items = data_manager.get("economy", "shop items")

        if item.lower() in shop_items:
            price = shop_items[item.lower()]["price"]
        else:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> Can't buy that item, because it doesn't exist",
                    colour=discord.Colour.red(),
                )
            )
        user_data: UserData = await data_manager.get_user_data(interaction.user.id)
        economy_items = data_manager.get("economy", "items")

        if (int(amount) * price) > user_data["balance"]:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You dont have enough 🪙 to buy that item",
                    colour=discord.Colour.red(),
                )
            )

        if item.lower() not in data_manager.get("economy", "shop items"):
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> Can't buy that item, because it doesn't exist",
                    colour=discord.Colour.red(),
                )
            )

        await data_manager.edit_user_data(
            interaction.user.id, "balance", user_data["balance"] - (int(amount) * price)
        )
        await data_manager.edit_user_inventory(
            interaction.user.id, item.lower(), +int(amount)
        )
        await interaction.response.send_message(
            embed=discord.Embed(
                description=f"{interaction.user.mention} Bought {amount} **{economy_items[item.lower()]["emoji"]} {string.capwords(item.lower())}** and paid **{(int(amount) * price)}** 🪙",
                colour=discord.Colour.from_rgb(43, 45, 49),
            )
            .set_author(
                name=f"Successful {string.capwords(item.lower())} Purchase",
                icon_url=interaction.user.display_avatar,
            )
            .set_footer(text="Thank you for your purchase!")
        )

    async def items_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        items = data_manager.get("economy", "items").keys()

        item_list = [
            app_commands.Choice(name=item, value=item)
            for item in items
            if item.lower().startswith(current.lower()) or len(current) < 1
        ]

        return item_list[0:25]

    @app_commands.command(name="info", description="View the description of an item")
    @app_commands.autocomplete(item=items_autocomplete)
    @app_commands.checks.cooldown(1, 15, key=lambda i: (i.user.id))
    @app_commands.describe(item="The item you want to view")
    async def item_info(self, interaction: discord.Interaction, item: str):
        if item not in data_manager.get("economy", "items"):
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> Can't find that item, because it doesn't exist",
                    colour=discord.Colour.red(),
                )
            )

        user_data: UserData = await data_manager.get_user_data(interaction.user.id)
        item1 = data_manager.get("economy", "items")[item.lower()]
        emoji = self.bot.get_emoji(item1["emoji_id"])
        whole_balance = user_data["balance"] + user_data["bank"]
        user_inv = user_data["inventory"]
        economy_items = data_manager.get("economy", "items")
        for item_owned in json.loads(user_inv):
            whole_balance += (
                economy_items[item.lower()]["sell price"]
                * json.loads(user_inv)[item_owned]
            )

        if user_inv is not None:
            inv = json.loads(user_inv)
            if item.lower() in inv:
                itemsowned = inv[item.lower()]
            else:
                itemsowned = 0
        else:
            itemsowned = 0

        if whole_balance != 0:
            percentage_of_net = (itemsowned * item1["sell price"]) / whole_balance * 100
        else:
            percentage_of_net = 0

        embed = discord.Embed(
            title=f"{item1['name']}",
            description=f"> {item1['description']} \n\n"
            f"You own **{itemsowned}** "
            + (
                f"({percentage_of_net:.1f}% of your net worth) \n"
                if percentage_of_net > 0
                else "\n"
            )
            + f"Sell Value: {item1['sell price']} 🪙\n"
            + (
                f"Shop Value: {item1['buy price']} 🪙"
                if item1["buy price"] != 0
                else "Can not be bought from the shop"
            ),
            colour=discord.Colour.from_rgb(15, 255, 255),
            url="https://github.com/Majestic-dev/Tester69",
        )

        embed.set_footer(text=item1["type"])
        embed.set_thumbnail(url=emoji.url)

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(item(bot))