from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from utils import data_manager

class banking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="pay", description="Pay someone some 🪙")
    @app_commands.checks.cooldown(1, 600, key=lambda i: (i.user.id))
    @app_commands.describe(
        user="The user you want to send the money to",
        amount="The amount of money you want to send",
    )
    async def pay(
        self, interaction: discord.Interaction, user: discord.User, amount: int
    ):
        if user.id == interaction.user.id:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You can't pay yourself!",
                    colour=discord.Colour.red(),
                )
            )

        if amount <= 0:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You can't pay someone a negative amount!",
                    colour=discord.Colour.red(),
                )
            )

        payer_data = await data_manager.get_user_data(interaction.user.id)
        if payer_data["balance"] < amount:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You don't have enough 🪙 to pay that amount!",
                    colour=discord.Colour.red(),
                )
            )

        await data_manager.edit_user_data(
            interaction.user.id, "balance", payer_data["balance"] - amount
        )

        receiver_data = await data_manager.get_user_data(user.id)
        await data_manager.edit_user_data(
            user.id, "balance", receiver_data["balance"] + amount
        )

        payer_data = await data_manager.get_user_data(interaction.user.id)

        await interaction.response.send_message(
            embed=discord.Embed(
                description=f'<:white_checkmark:1096793014287995061> Paid {user.mention} {amount} 🪙. Your new balance is {payer_data["balance"]} 🪙',
                colour=discord.Colour.green(),
            )
        )


    @app_commands.command(name="balance", description="Check your 🪙 balance")
    @app_commands.checks.cooldown(1, 20, key=lambda i: (i.user.id))
    @app_commands.describe(
        user="The user you want to check the balance of (yours if no user is provided)"
    )
    async def balance(
        self, interaction: discord.Interaction, user: Optional[discord.User] = None
    ):
        await interaction.response.defer()
        if user == None:
            user_data = await data_manager.get_user_data(interaction.user.id)
            await interaction.edit_original_response(
                embed=discord.Embed(
                    title=f"{interaction.user}'s Balance",
                    description=(
                        f'**💵 Wallet:** {user_data["balance"]} 🪙\n**🏦 Bank:** {user_data["bank"]} 🪙'
                    ),
                    colour=discord.Colour.green(),
                )
            )
        else:
            user_data = await data_manager.get_user_data(user.id)
            await interaction.edit_original_response(
                embed=discord.Embed(
                    title=f"{user}'s Balance",
                    description=(
                        f'**💵 Wallet:** {user_data["balance"]} 🪙\n**🏦 Bank:** {user_data["bank"]} 🪙'
                    ),
                    colour=discord.Colour.green(),
                )
            )

    @app_commands.command(name="deposit", description="Deposit money into your bank")
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    @app_commands.describe(amount="The amount of 🪙 you want to deposit")
    async def deposit(self, interaction: discord.Interaction, amount: str):
        user_data = await data_manager.get_user_data(interaction.user.id)

        if amount == "all":
            if user_data["balance"] != 0:
                await data_manager.edit_user_data(
                    interaction.user.id,
                    "bank",
                    user_data["bank"] + user_data["balance"],
                )
                await data_manager.edit_user_data(
                    interaction.user.id,
                    "balance",
                    user_data["balance"] - user_data["balance"],
                )
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        description="<:white_checkmark:1096793014287995061> Deposited all your 🪙 in the bank",
                        colour=discord.Colour.green(),
                    )
                )
            else:
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        description="<:white_cross:1096791282023669860> You don't have any 🪙 to deposit",
                        colour=discord.Colour.orange(),
                    )
                )

        if amount.isnumeric() == False:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> Enter a valid number as an input",
                    colour=discord.Colour.red(),
                )
            )

        if int(amount) > user_data["balance"]:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You do not have enough money to deposit",
                    colour=discord.Colour.orange(),
                )
            )

        await data_manager.edit_user_data(
            interaction.user.id, "balance", user_data["balance"] - int(amount)
        )
        await data_manager.edit_user_data(
            interaction.user.id, "bank", user_data["bank"] + int(amount)
        )

        await interaction.response.send_message(
            embed=discord.Embed(
                description=f"<:white_checkmark:1096793014287995061> Deposited {amount} 🪙 into your bank",
                colour=discord.Colour.green(),
            )
        )

    @app_commands.command(name="withdraw", description="Withdraw money from your bank")
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    @app_commands.describe(amount="The amount of 🪙 you want to withdraw")
    async def withdraw(self, interaction: discord.Interaction, amount: str):
        user_data = await data_manager.get_user_data(interaction.user.id)

        if amount == "all":
            await data_manager.edit_user_data(
                interaction.user.id, "balance", user_data["balance"] + user_data["bank"]
            )
            await data_manager.edit_user_data(
                interaction.user.id, "bank", user_data["bank"] - user_data["bank"]
            )
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_checkmark:1096793014287995061> Withdrew all your 🪙 from the bank",
                    colour=discord.Colour.green(),
                )
            )

        if amount.isnumeric() == False:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> Enter a valid number as an input",
                    colour=discord.Colour.red(),
                )
            )

        if int(amount) > user_data["bank"]:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You do not have enough money to withdraw",
                    colour=discord.Colour.orange(),
                )
            )

        await data_manager.edit_user_data(
            interaction.user.id, "bank", user_data["bank"] - int(amount)
        )
        await data_manager.edit_user_data(
            interaction.user.id, "balance", user_data["balance"] + int(amount)
        )

        await interaction.response.send_message(
            embed=discord.Embed(
                description=f"<:white_checkmark:1096793014287995061> Withdrew {int(amount)} 🪙 from your bank",
                colour=discord.Colour.green(),
            )
        )