import discord
import json
import datetime

from discord import app_commands
from discord.ext import commands, tasks

from utils import data_manager, UserData, CraftingData


craftable_items = data_manager.get("crafting_recipes", "recipes")
items = data_manager.get("economy", "items")
selected_item = list(craftable_items.keys())[0]

options = []
for i in craftable_items:
    options.append(
        discord.SelectOption(
            label=i, description=items[i.lower()]["description"], emoji=items[i.lower()]["emoji"], default=(i==selected_item)
        )
    )

async def can_craft(inv: dict, recipe: dict):
    for item in recipe:
        if inv.get(item, 0) < recipe[item]:
            return False
    return True

async def format_craft_time(minutes: int) -> str:
    hours, mins = divmod(minutes, 60)
    parts = []

    if hours:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if mins:
        parts.append(f"{mins} minute{'s' if mins != 1 else ''}")
    return " and ".join(parts) if parts else "0 minutes"

class craftingview(discord.ui.View):
    def __init__(self, bot: commands.AutoShardedBot, executor_id: int, interaction: discord.Interaction):
        self.bot = bot
        self.executor_id = executor_id
        self.interaction = interaction
        self.selected_item = selected_item

        super().__init__()

    @discord.ui.button(label="Craft", style=discord.ButtonStyle.green, row=1)
    async def craft_callback(
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
        user_crafting: CraftingData = await data_manager.get_user_crafting(interaction.user.id)
        inv = json.loads(user_data["inventory"])
        now = discord.utils.utcnow().isoformat()

        if user_crafting["end_date"] == None:
            if await can_craft(inv=inv, recipe=craftable_items[self.selected_item]):
                for item in craftable_items[self.selected_item]:
                    inv[item] -= craftable_items[self.selected_item][item]

                await data_manager.edit_user_data(interaction.user.id, "inventory", json.dumps(inv))
                minutes = items[self.selected_item]["crafting_time"]

                await data_manager.add_crafting(interaction.user.id, self.selected_item, minutes)

                await interaction.followup.send(
                    content=f"You started crafting a {self.selected_item}!",
                    ephemeral=True
                )
                
                emoji = self.bot.get_emoji(items[self.selected_item]["emoji_id"])
                return await interaction.edit_original_response(
                    embed=discord.Embed(
                    title=self.selected_item,
                    description=f"""
                        **Crafting time:**
                        {await format_craft_time(items[self.selected_item]["crafting_time"])}\n\n
                        **Components:**
                        {"\n".join((items[a]["emoji"] + f" `{inv.get(a, 0)}/{craftable_items[self.selected_item][a]}` *{a}*" for a in craftable_items[self.selected_item]))}
                        """
                ).set_thumbnail(url=emoji.url),
                view=self
            )

            elif not await can_craft(inv=inv, recipe=craftable_items[self.selected_item]):
                return await interaction.followup.send(
                    content=f"You do not have the items to craft a {self.selected_item}",
                    ephemeral=True
                )
            
        elif user_crafting["end_date"] > now:
            item = user_crafting["item"]
            end_date = discord.utils.format_dt(datetime.datetime.fromisoformat(user_crafting["end_date"]), style="R")
            return await interaction.followup.send(
                content=f"You are currently crafting a {items[item]["emoji"]}`{item}` which will be finished {end_date}",
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
            for i in craftable_items
        ]
        return await interaction.edit_original_response(
            embed=discord.Embed(
                title=self.selected_item,
                description=f"""
                    **Crafting time:**
                    {await format_craft_time(items[self.selected_item]["crafting_time"])}\n\n
                    **Components:**
                    {"\n".join((items[a]["emoji"] + f" `{user_inv.get(a, 0)}/{craftable_items[self.selected_item][a]}` *{a}*" for a in craftable_items[self.selected_item]))}
                    """
            ).set_thumbnail(url=emoji.url),
            view=self
        )



class crafting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.craftingloop.start()
    
    @tasks.loop(minutes=1)
    async def craftingloop(self):
        async with data_manager.db_connection.acquire():
            ended_craftings = await data_manager.db_connection.fetch(
                "SELECT * FROM crafting WHERE end_date < $1",
                discord.utils.utcnow().isoformat()
            )
            ended_craftings = [dict(craft) for craft in ended_craftings]

            for craft in ended_craftings:
                user_crafting = await data_manager.get_user_crafting(craft["user_id"])
                await data_manager.delete_crafting(craft["user_id"])
                await data_manager.edit_user_inventory(craft["user_id"], user_crafting["item"], 1)

    @app_commands.command(name="craft", description="Craft an item")
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    async def craft(self, interaction: discord.Interaction):
        user_data: UserData = await data_manager.get_user_data(interaction.user.id)
        user_inv = json.loads(user_data["inventory"])
        emoji = self.bot.get_emoji(items[selected_item]["emoji_id"])

        return await interaction.response.send_message(
            embed=discord.Embed(
                title=selected_item,
                description=f"""
                    **Crafting time:**
                    {await format_craft_time(items[selected_item]["crafting_time"])}\n\n
                    **Components:**
                    {"\n".join((items[a]["emoji"] + f" `{user_inv.get(a, 0)}/{craftable_items[selected_item][a]}` *{a}*" for a in craftable_items[selected_item]))}
                    """
            ).set_thumbnail(url=emoji.url),
            view=craftingview(self.bot, interaction.user.id, interaction)
        )

async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(crafting(bot))