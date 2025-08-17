import discord
import json
import datetime

from discord import app_commands
from discord.ext import commands, tasks

from utils import data_manager, UserData, ForgingData


forgable_items = data_manager.get("forging_recipes", "recipes")
items = data_manager.get("economy", "items")
selected_item = list(forgable_items.keys())[0]

options = []
for i in forgable_items:
    options.append(
        discord.SelectOption(
            label=i, description=items[i.lower()]["description"], emoji=items[i.lower()]["emoji"], default=(i==selected_item)
        )
    )

async def can_forge(inv: dict, recipe: dict):
    for item in recipe:
        if inv.get(item, 0) < recipe[item]:
            return False
    return True

async def format_forge_time(minutes: int) -> str:
    hours, mins = divmod(minutes, 60)
    parts = []

    if hours:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if mins:
        parts.append(f"{mins} minute{'s' if mins != 1 else ''}")
    return " and ".join(parts) if parts else "0 minutes"

class forgingview(discord.ui.View):
    def __init__(self, bot: commands.AutoShardedBot, executor_id: int, interaction: discord.Interaction):
        self.bot = bot
        self.executor_id = executor_id
        self.interaction = interaction
        self.selected_item = selected_item

        super().__init__()

    @discord.ui.button(label="Forge", emoji="🔥", style=discord.ButtonStyle.green, row=1)
    async def forge_callback(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.executor_id:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error",
                    description="You are not the executor of this command",
                    colour=discord.Colour.red(),
                ),
                ephemeral=True,
            )
        
        await interaction.response.defer(ephemeral=True)
        user_data: UserData = await data_manager.get_user_data(interaction.user.id)
        user_forging: ForgingData = await data_manager.get_user_forging(interaction.user.id)
        inv = json.loads(user_data["inventory"])
        now = discord.utils.utcnow().isoformat()

        if user_forging["end_date"] == None:
            if await can_forge(inv=inv, recipe=forgable_items[self.selected_item]):
                for item in forgable_items[self.selected_item]:
                    inv[item] -= forgable_items[self.selected_item][item]

                await data_manager.edit_user_data(interaction.user.id, "inventory", json.dumps(inv))
                minutes = items[self.selected_item]["forging_time"]

                await data_manager.add_forging(interaction.user.id, self.selected_item, minutes)

                await interaction.followup.send(
                    content=f"You started forging a {self.selected_item}!",
                    ephemeral=True
                )
                
                emoji = self.bot.get_emoji(items[self.selected_item]["emoji_id"])
                return await interaction.edit_original_response(
                    embed=discord.Embed(
                    title=self.selected_item,
                    description=f"""
                        **Forging time:**
                        {await format_forge_time(items[self.selected_item]["forging_time"])}\n\n
                        **Components:**
                        {"\n".join((items[a]["emoji"] + f" `{inv.get(a, 0)}/{forgable_items[self.selected_item][a]}` *{a}*" for a in forgable_items[self.selected_item]))}
                        """
                ).set_thumbnail(url=emoji.url),
                view=self
            )

            elif not await can_forge(inv=inv, recipe=forgable_items[self.selected_item]):
                return await interaction.followup.send(
                    content=f"You do not have the items to forge this item",
                    ephemeral=True
                )
            
        elif user_forging["end_date"] > now:
            item = user_forging["item"]
            end_date = discord.utils.format_dt(datetime.datetime.fromisoformat(user_forging["end_date"]), style="R")
            return await interaction.followup.send(
                content=f"You are currently forging a {items[item]["emoji"]}`{item}` which will be finished {end_date}",
                ephemeral=True
            )


    @discord.ui.select(options=options, max_values=1, min_values=1, row=0)
    async def select_item_callback(
        self, interaction: discord.Interaction, select: discord.ui.Select
    ):
        if interaction.user.id != self.executor_id:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error",
                    description="You are not the executor of this command",
                    colour=discord.Colour.red(),
                ),
                ephemeral=True,
            )
        
        await interaction.response.defer(ephemeral=True)
        user_data: UserData = await data_manager.get_user_data(interaction.user.id)
        user_inv = json.loads(user_data["inventory"])
        self.selected_item = select.values[0]
        emoji = self.bot.get_emoji(items[self.selected_item]["emoji_id"])
        select.options = [
            discord.SelectOption(
                label=i, description=items[i.lower()]["description"], emoji=items[i.lower()]["emoji"], default=(i==self.selected_item)
            )
            for i in forgable_items
        ]
        return await interaction.edit_original_response(
            embed=discord.Embed(
                title=self.selected_item,
                description=f"""
                    **Forging time:**
                    {await format_forge_time(items[self.selected_item]["forging_time"])}\n\n
                    **Components:**
                    {"\n".join((items[a]["emoji"] + f" `{user_inv.get(a, 0)}/{forgable_items[self.selected_item][a]}` *{a}*" for a in forgable_items[self.selected_item]))}
                    """
            ).set_thumbnail(url=emoji.url),
            view=self
        )



class forging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.forgingloop.start()
    
    @tasks.loop(minutes=1)
    async def forgingloop(self):
        async with data_manager.db_connection.acquire():
            ended_forgings = await data_manager.db_connection.fetch(
                "SELECT * FROM forging WHERE end_date < $1",
                discord.utils.utcnow().isoformat()
            )
            ended_forgings = [dict(forge) for forge in ended_forgings]

            for forge in ended_forgings:
                user_forging = await data_manager.get_user_forging(forge["user_id"])
                await data_manager.delete_forging(forge["user_id"])
                await data_manager.edit_user_inventory(forge["user_id"], user_forging["item"], 1)

    @app_commands.command(name="forge", description="Forge an item")
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    async def forge(self, interaction: discord.Interaction):
        user_data: UserData = await data_manager.get_user_data(interaction.user.id)
        user_inv = json.loads(user_data["inventory"])
        emoji = self.bot.get_emoji(items[selected_item]["emoji_id"])

        return await interaction.response.send_message(
            embed=discord.Embed(
                title=selected_item,
                description=f"""
                    **Forging time:**
                    {await format_forge_time(items[selected_item]["forging_time"])}\n\n
                    **Components:**
                    {"\n".join((items[a]["emoji"] + f" `{user_inv.get(a, 0)}/{forgable_items[selected_item][a]}` *{a}*" for a in forgable_items[selected_item]))}
                    """
            ).set_thumbnail(url=emoji.url),
            view=forgingview(self.bot, interaction.user.id, interaction)
        )

async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(forging(bot))