import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import random
import time
from utils import DataManager, cooldown_check


async def find_user_level(user_id: int):
    user_data = await DataManager.get_user_data(user_id)
    if user_data["mining_xp"] == None:
        return 0
    levels = DataManager.get("levels", "levels")
    for level in levels:
        required_xp = levels[level]["requiredXP"]
        if user_data["mining_xp"] < required_xp:
            return int(level) - 1
        elif user_data["mining_xp"] == required_xp:
            return int(level)
    return 50


class mining_buttons(discord.ui.View):
    def __init__(self, bot, mine: str):
        super().__init__(timeout=60)

        self.bot = bot
        self.response: discord.Message = None
        self.mine_name = mine
        self.mine = DataManager.get("mines", mine)
        self.max_ores: dict = {}
        self.ore_positions: dict = {}
        self.ores = DataManager.get("ores", "ores")
        self.mined_ores = 0
        self.mined_items = {}
        self.gained_xp = 0
        self.button_clicked = False
        self.closed = False

        random.seed(time.time())

        positions = list(range(1, 26))
        random.shuffle(positions)

        ores = []
        for ore in self.mine["resources"]:
            min_ore = int(self.mine["resources"][ore]["min"])
            max_ore = int(self.mine["resources"][ore]["max"])
            ore_count = random.randint(min_ore, max_ore)
            ores.extend([ore] * ore_count)
        random.shuffle(ores)

        for position, ore in zip(positions, ores):
            self.max_ores[ore] = ore_count
            self.ore_positions[position] = ore

    @discord.ui.button(style=discord.ButtonStyle.gray, label="⠀", disabled=False, row=0)
    async def first(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.first.disabled = True

        if not self.closed:
            if 1 in self.ore_positions:
                self.mined_ores += 1
                self.first.label = None
                self.first.emoji = self.ores[self.ore_positions[1]]["emoji"]

                xp = self.ores[self.ore_positions[1]]["xp"]
                self.gained_xp += xp

                ore = self.ore_positions[1]
                if ore in self.mined_items:
                    self.mined_items[ore] += 1
                else:
                    self.mined_items[ore] = 1

            await interaction.edit_original_response(view=self)

            if not self.button_clicked:
                self.button_clicked = True

                await asyncio.sleep(17)
                self.closed = True

                if self.mined_ores == len(self.ore_positions):
                    pass
                else:
                    user_data = await DataManager.get_user_data(interaction.user.id)
                    mining_xp = user_data["mining_xp"]
                    if mining_xp == None:
                        mining_xp = 0

                    await DataManager.edit_user_data(
                        interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                    )

                    return await interaction.edit_original_response(
                        embed=discord.Embed(
                            title="The mine crumbles down!",
                            description=f"As the {self.mine_name} crumbles down, you are forced to leave.",
                            colour=discord.Colour.from_rgb(139, 69, 19),
                        )
                    )

            if self.mined_ores == len(self.ore_positions):
                await interaction.edit_original_response(
                    embed=discord.Embed(
                        title="You have mined all the ores!",
                        description="You have mined all the ores in the mine, you are forced to leave.",
                        colour=discord.Colour.from_rgb(139, 69, 19),
                    ),
                    view=None,
                )

                user_data = await DataManager.get_user_data(interaction.user.id)
                mining_xp = user_data["mining_xp"]
                if mining_xp == None:
                    mining_xp = 0

                await DataManager.edit_user_data(
                    interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                )

                for ore, quantity in self.mined_items.items():
                    await DataManager.edit_user_inventory(
                        interaction.user.id, ore, quantity
                    )

    @discord.ui.button(style=discord.ButtonStyle.gray, label="⠀", row=0)
    async def second(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.second.disabled = True

        if not self.closed:
            if 2 in self.ore_positions:
                self.mined_ores += 1
                self.second.label = None
                self.second.emoji = self.ores[self.ore_positions[2]]["emoji"]

                xp = self.ores[self.ore_positions[2]]["xp"]
                self.gained_xp += xp

                ore = self.ore_positions[2]
                if ore in self.mined_items:
                    self.mined_items[ore] += 1
                else:
                    self.mined_items[ore] = 1

            await interaction.edit_original_response(view=self)

            if not self.button_clicked:
                self.button_clicked = True

                await asyncio.sleep(17)
                self.closed = True

                if self.mined_ores == len(self.ore_positions):
                    pass
                else:
                    user_data = await DataManager.get_user_data(interaction.user.id)
                    mining_xp = user_data["mining_xp"]
                    if mining_xp == None:
                        mining_xp = 0

                    await DataManager.edit_user_data(
                        interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                    )

                    return await interaction.edit_original_response(
                        embed=discord.Embed(
                            title="The mine crumbles down!",
                            description=f"As the {self.mine_name} crumbles down, you are forced to leave.",
                            colour=discord.Colour.from_rgb(139, 69, 19),
                        ),
                        view=None,
                    )

            if self.mined_ores == len(self.ore_positions):
                await interaction.edit_original_response(
                    embed=discord.Embed(
                        title="You have mined all the ores!",
                        description="You have mined all the ores in the mine, you are forced to leave.",
                        colour=discord.Colour.from_rgb(139, 69, 19),
                    ),
                    view=None,
                )

                user_data = await DataManager.get_user_data(interaction.user.id)
                mining_xp = user_data["mining_xp"]
                if mining_xp == None:
                    mining_xp = 0

                await DataManager.edit_user_data(
                    interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                )

                for ore, quantity in self.mined_items.items():
                    await DataManager.edit_user_inventory(
                        interaction.user.id, ore, quantity
                    )

    @discord.ui.button(style=discord.ButtonStyle.gray, label="⠀", row=0)
    async def third(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.third.disabled = True

        if not self.closed:
            if 3 in self.ore_positions:
                self.mined_ores += 1
                self.third.label = None
                self.third.emoji = self.ores[self.ore_positions[3]]["emoji"]

                xp = self.ores[self.ore_positions[3]]["xp"]
                self.gained_xp += xp

                ore = self.ore_positions[3]
                if ore in self.mined_items:
                    self.mined_items[ore] += 1
                else:
                    self.mined_items[ore] = 1

            await interaction.edit_original_response(view=self)

            if not self.button_clicked:
                self.button_clicked = True

                await asyncio.sleep(17)
                self.closed = True

                if self.mined_ores == len(self.ore_positions):
                    pass
                else:
                    user_data = await DataManager.get_user_data(interaction.user.id)
                    mining_xp = user_data["mining_xp"]
                    if mining_xp == None:
                        mining_xp = 0

                    await DataManager.edit_user_data(
                        interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                    )

                    return await interaction.edit_original_response(
                        embed=discord.Embed(
                            title="The mine crumbles down!",
                            description=f"As the {self.mine_name} crumbles down, you are forced to leave.",
                            colour=discord.Colour.from_rgb(139, 69, 19),
                        ),
                        view=None,
                    )

            if self.mined_ores == len(self.ore_positions):
                await interaction.edit_original_response(
                    embed=discord.Embed(
                        title="You have mined all the ores!",
                        description="You have mined all the ores in the mine, you are forced to leave.",
                        colour=discord.Colour.from_rgb(139, 69, 19),
                    ),
                    view=None,
                )

                user_data = await DataManager.get_user_data(interaction.user.id)
                mining_xp = user_data["mining_xp"]
                if mining_xp == None:
                    mining_xp = 0

                await DataManager.edit_user_data(
                    interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                )

    @discord.ui.button(style=discord.ButtonStyle.gray, label="⠀", row=0)
    async def fourth(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.fourth.disabled = True

        if not self.closed:
            if 4 in self.ore_positions:
                self.mined_ores += 1
                self.fourth.label = None
                self.fourth.emoji = self.ores[self.ore_positions[4]]["emoji"]

                xp = self.ores[self.ore_positions[4]]["xp"]
                self.gained_xp += xp

                ore = self.ore_positions[4]
                if ore in self.mined_items:
                    self.mined_items[ore] += 1
                else:
                    self.mined_items[ore] = 1

            await interaction.edit_original_response(view=self)

            if not self.button_clicked:
                self.button_clicked = True

                await asyncio.sleep(17)
                self.closed = True

                if self.mined_ores == len(self.ore_positions):
                    pass
                else:
                    user_data = await DataManager.get_user_data(interaction.user.id)
                    mining_xp = user_data["mining_xp"]
                    if mining_xp == None:
                        mining_xp = 0

                    await DataManager.edit_user_data(
                        interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                    )

                    for ore, quantity in self.mined_items.items():
                        await DataManager.edit_user_inventory(
                            interaction.user.id, ore, quantity
                        )
                    for ore, quantity in self.mined_items.items():
                        await DataManager.edit_user_inventory(
                            interaction.user.id, ore, quantity
                        )

                    return await interaction.edit_original_response(
                        embed=discord.Embed(
                            title="The mine crumbles down!",
                            description=f"As the {self.mine_name} crumbles down, you are forced to leave.",
                            colour=discord.Colour.from_rgb(139, 69, 19),
                        ),
                        view=None,
                    )

            if self.mined_ores == len(self.ore_positions):
                await interaction.edit_original_response(
                    embed=discord.Embed(
                        title="You have mined all the ores!",
                        description="You have mined all the ores in the mine, you are forced to leave.",
                        colour=discord.Colour.from_rgb(139, 69, 19),
                    ),
                    view=None,
                )

                user_data = await DataManager.get_user_data(interaction.user.id)
                mining_xp = user_data["mining_xp"]
                if mining_xp == None:
                    mining_xp = 0

                await DataManager.edit_user_data(
                    interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                )

    @discord.ui.button(style=discord.ButtonStyle.gray, label="⠀", row=0)
    async def fifth(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.fifth.disabled = True

        if not self.closed:
            if 5 in self.ore_positions:
                self.mined_ores += 1
                self.fifth.label = None
                self.fifth.emoji = self.ores[self.ore_positions[5]]["emoji"]

                xp = self.ores[self.ore_positions[5]]["xp"]
                self.gained_xp += xp

                ore = self.ore_positions[5]
                if ore in self.mined_items:
                    self.mined_items[ore] += 1
                else:
                    self.mined_items[ore] = 1

            await interaction.edit_original_response(view=self)

            if not self.button_clicked:
                self.button_clicked = True

                await asyncio.sleep(17)
                self.closed = True

                if self.mined_ores == len(self.ore_positions):
                    pass
                else:
                    user_data = await DataManager.get_user_data(interaction.user.id)
                    mining_xp = user_data["mining_xp"]
                    if mining_xp == None:
                        mining_xp = 0

                    await DataManager.edit_user_data(
                        interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                    )

                    for ore, quantity in self.mined_items.items():
                        await DataManager.edit_user_inventory(
                            interaction.user.id, ore, quantity
                        )

                    return await interaction.edit_original_response(
                        embed=discord.Embed(
                            title="The mine crumbles down!",
                            description=f"As the {self.mine_name} crumbles down, you are forced to leave.",
                            colour=discord.Colour.from_rgb(139, 69, 19),
                        ),
                        view=None,
                    )

            if self.mined_ores == len(self.ore_positions):
                await interaction.edit_original_response(
                    embed=discord.Embed(
                        title="You have mined all the ores!",
                        description="You have mined all the ores in the mine, you are forced to leave.",
                        colour=discord.Colour.from_rgb(139, 69, 19),
                    ),
                    view=None,
                )

                user_data = await DataManager.get_user_data(interaction.user.id)
                mining_xp = user_data["mining_xp"]
                if mining_xp == None:
                    mining_xp = 0

                await DataManager.edit_user_data(
                    interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                )

    @discord.ui.button(style=discord.ButtonStyle.gray, label="⠀", row=1)
    async def sixth(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.sixth.disabled = True

        if not self.closed:
            if 6 in self.ore_positions:
                self.mined_ores += 1
                self.sixth.label = None
                self.sixth.emoji = self.ores[self.ore_positions[6]]["emoji"]

                xp = self.ores[self.ore_positions[6]]["xp"]
                self.gained_xp += xp

                ore = self.ore_positions[6]
                if ore in self.mined_items:
                    self.mined_items[ore] += 1
                else:
                    self.mined_items[ore] = 1

            await interaction.edit_original_response(view=self)
            if not self.button_clicked:
                self.button_clicked = True

                await asyncio.sleep(17)
                self.closed = True

                if self.mined_ores == len(self.ore_positions):
                    pass
                else:
                    user_data = await DataManager.get_user_data(interaction.user.id)
                    mining_xp = user_data["mining_xp"]
                    if mining_xp == None:
                        mining_xp = 0

                    await DataManager.edit_user_data(
                        interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                    )

                    for ore, quantity in self.mined_items.items():
                        await DataManager.edit_user_inventory(
                            interaction.user.id, ore, quantity
                        )

                    return await interaction.edit_original_response(
                        embed=discord.Embed(
                            title="The mine crumbles down!",
                            description=f"As the {self.mine_name} crumbles down, you are forced to leave.",
                            colour=discord.Colour.from_rgb(139, 69, 19),
                        ),
                        view=None,
                    )

            if self.mined_ores == len(self.ore_positions):
                await interaction.edit_original_response(
                    embed=discord.Embed(
                        title="You have mined all the ores!",
                        description="You have mined all the ores in the mine, you are forced to leave.",
                        colour=discord.Colour.from_rgb(139, 69, 19),
                    ),
                    view=None,
                )

                user_data = await DataManager.get_user_data(interaction.user.id)
                mining_xp = user_data["mining_xp"]
                if mining_xp == None:
                    mining_xp = 0

                await DataManager.edit_user_data(
                    interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                )

    @discord.ui.button(style=discord.ButtonStyle.gray, label="⠀", row=1)
    async def seventh(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer()
        self.seventh.disabled = True

        if not self.closed:
            if 7 in self.ore_positions:
                self.mined_ores += 1
                self.seventh.label = None
                self.seventh.emoji = self.ores[self.ore_positions[7]]["emoji"]

                xp = self.ores[self.ore_positions[7]]["xp"]
                self.gained_xp += xp

                ore = self.ore_positions[7]
                if ore in self.mined_items:
                    self.mined_items[ore] += 1
                else:
                    self.mined_items[ore] = 1

            await interaction.edit_original_response(view=self)
            if not self.button_clicked:
                self.button_clicked = True

                await asyncio.sleep(17)
                self.closed = True

                if self.mined_ores == len(self.ore_positions):
                    pass
                else:
                    user_data = await DataManager.get_user_data(interaction.user.id)
                    mining_xp = user_data["mining_xp"]
                    if mining_xp == None:
                        mining_xp = 0

                    await DataManager.edit_user_data(
                        interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                    )

                    for ore, quantity in self.mined_items.items():
                        await DataManager.edit_user_inventory(
                            interaction.user.id, ore, quantity
                        )

                    return await interaction.edit_original_response(
                        embed=discord.Embed(
                            title="The mine crumbles down!",
                            description=f"As the {self.mine_name} crumbles down, you are forced to leave.",
                            colour=discord.Colour.from_rgb(139, 69, 19),
                        ),
                        view=None,
                    )

            if self.mined_ores == len(self.ore_positions):
                await interaction.edit_original_response(
                    embed=discord.Embed(
                        title="You have mined all the ores!",
                        description="You have mined all the ores in the mine, you are forced to leave.",
                        colour=discord.Colour.from_rgb(139, 69, 19),
                    ),
                    view=None,
                )

                user_data = await DataManager.get_user_data(interaction.user.id)
                mining_xp = user_data["mining_xp"]
                if mining_xp == None:
                    mining_xp = 0

                await DataManager.edit_user_data(
                    interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                )

    @discord.ui.button(style=discord.ButtonStyle.gray, label="⠀", row=1)
    async def eighth(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.eighth.disabled = True

        if not self.closed:
            if 8 in self.ore_positions:
                self.mined_ores += 1
                self.eighth.label = None
                self.eighth.emoji = self.ores[self.ore_positions[8]]["emoji"]

                xp = self.ores[self.ore_positions[8]]["xp"]
                self.gained_xp += xp

                ore = self.ore_positions[8]
                if ore in self.mined_items:
                    self.mined_items[ore] += 1
                else:
                    self.mined_items[ore] = 1

            await interaction.edit_original_response(view=self)
            if not self.button_clicked:
                self.button_clicked = True

                await asyncio.sleep(17)
                self.closed = True

                if self.mined_ores == len(self.ore_positions):
                    pass
                else:
                    user_data = await DataManager.get_user_data(interaction.user.id)
                    mining_xp = user_data["mining_xp"]
                    if mining_xp == None:
                        mining_xp = 0

                    await DataManager.edit_user_data(
                        interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                    )

                    for ore, quantity in self.mined_items.items():
                        await DataManager.edit_user_inventory(
                            interaction.user.id, ore, quantity
                        )

                    return await interaction.edit_original_response(
                        embed=discord.Embed(
                            title="The mine crumbles down!",
                            description=f"As the {self.mine_name} crumbles down, you are forced to leave.",
                            colour=discord.Colour.from_rgb(139, 69, 19),
                        ),
                        view=None,
                    )

            if self.mined_ores == len(self.ore_positions):
                await interaction.edit_original_response(
                    embed=discord.Embed(
                        title="You have mined all the ores!",
                        description="You have mined all the ores in the mine, you are forced to leave.",
                        colour=discord.Colour.from_rgb(139, 69, 19),
                    ),
                    view=None,
                )

                user_data = await DataManager.get_user_data(interaction.user.id)
                mining_xp = user_data["mining_xp"]
                if mining_xp == None:
                    mining_xp = 0

                await DataManager.edit_user_data(
                    interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                )

    @discord.ui.button(style=discord.ButtonStyle.gray, label="⠀", row=1)
    async def ninth(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.ninth.disabled = True

        if not self.closed:
            if 9 in self.ore_positions:
                self.mined_ores += 1
                self.ninth.label = None
                self.ninth.emoji = self.ores[self.ore_positions[9]]["emoji"]

                xp = self.ores[self.ore_positions[9]]["xp"]
                self.gained_xp += xp

                ore = self.ore_positions[9]
                if ore in self.mined_items:
                    self.mined_items[ore] += 1
                else:
                    self.mined_items[ore] = 1

            await interaction.edit_original_response(view=self)
            if not self.button_clicked:
                self.button_clicked = True

                await asyncio.sleep(17)
                self.closed = True

                if self.mined_ores == len(self.ore_positions):
                    pass
                else:
                    user_data = await DataManager.get_user_data(interaction.user.id)
                    mining_xp = user_data["mining_xp"]
                    if mining_xp == None:
                        mining_xp = 0

                    await DataManager.edit_user_data(
                        interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                    )

                    for ore, quantity in self.mined_items.items():
                        await DataManager.edit_user_inventory(
                            interaction.user.id, ore, quantity
                        )

                    return await interaction.edit_original_response(
                        embed=discord.Embed(
                            title="The mine crumbles down!",
                            description=f"As the {self.mine_name} crumbles down, you are forced to leave.",
                            colour=discord.Colour.from_rgb(139, 69, 19),
                        ),
                        view=None,
                    )

            if self.mined_ores == len(self.ore_positions):
                await interaction.edit_original_response(
                    embed=discord.Embed(
                        title="You have mined all the ores!",
                        description="You have mined all the ores in the mine, you are forced to leave.",
                        colour=discord.Colour.from_rgb(139, 69, 19),
                    ),
                    view=None,
                )

                user_data = await DataManager.get_user_data(interaction.user.id)
                mining_xp = user_data["mining_xp"]
                if mining_xp == None:
                    mining_xp = 0

                await DataManager.edit_user_data(
                    interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                )

    @discord.ui.button(style=discord.ButtonStyle.gray, label="⠀", row=1)
    async def tenth(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.tenth.disabled = True

        if not self.closed:
            if 10 in self.ore_positions:
                self.mined_ores += 1
                self.tenth.label = None
                self.tenth.emoji = self.ores[self.ore_positions[10]]["emoji"]

                xp = self.ores[self.ore_positions[10]]["xp"]
                self.gained_xp += xp

                ore = self.ore_positions[10]
                if ore in self.mined_items:
                    self.mined_items[ore] += 1
                else:
                    self.mined_items[ore] = 1

            await interaction.edit_original_response(view=self)
            if not self.button_clicked:
                self.button_clicked = True

                await asyncio.sleep(17)
                self.closed = True

                if self.mined_ores == len(self.ore_positions):
                    pass
                else:
                    user_data = await DataManager.get_user_data(interaction.user.id)
                    mining_xp = user_data["mining_xp"]
                    if mining_xp == None:
                        mining_xp = 0

                    await DataManager.edit_user_data(
                        interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                    )

                    for ore, quantity in self.mined_items.items():
                        await DataManager.edit_user_inventory(
                            interaction.user.id, ore, quantity
                        )

                    return await interaction.edit_original_response(
                        embed=discord.Embed(
                            title="The mine crumbles down!",
                            description=f"As the {self.mine_name} crumbles down, you are forced to leave.",
                            colour=discord.Colour.from_rgb(139, 69, 19),
                        ),
                        view=None,
                    )

            if self.mined_ores == len(self.ore_positions):
                await interaction.edit_original_response(
                    embed=discord.Embed(
                        title="You have mined all the ores!",
                        description="You have mined all the ores in the mine, you are forced to leave.",
                        colour=discord.Colour.from_rgb(139, 69, 19),
                    ),
                    view=None,
                )

                user_data = await DataManager.get_user_data(interaction.user.id)
                mining_xp = user_data["mining_xp"]
                if mining_xp == None:
                    mining_xp = 0

                await DataManager.edit_user_data(
                    interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                )

    @discord.ui.button(style=discord.ButtonStyle.gray, label="⠀", row=2)
    async def eleventh(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer()
        self.eleventh.disabled = True

        if not self.closed:
            if 11 in self.ore_positions:
                self.mined_ores += 1
                self.eleventh.label = None
                self.eleventh.emoji = self.ores[self.ore_positions[11]]["emoji"]

                xp = self.ores[self.ore_positions[11]]["xp"]
                self.gained_xp += xp

                ore = self.ore_positions[11]
                if ore in self.mined_items:
                    self.mined_items[ore] += 1
                else:
                    self.mined_items[ore] = 1

            await interaction.edit_original_response(view=self)
            if not self.button_clicked:
                self.button_clicked = True

                await asyncio.sleep(17)
                self.closed = True

                if self.mined_ores == len(self.ore_positions):
                    pass
                else:
                    user_data = await DataManager.get_user_data(interaction.user.id)
                    mining_xp = user_data["mining_xp"]
                    if mining_xp == None:
                        mining_xp = 0

                    await DataManager.edit_user_data(
                        interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                    )

                    for ore, quantity in self.mined_items.items():
                        await DataManager.edit_user_inventory(
                            interaction.user.id, ore, quantity
                        )

                    return await interaction.edit_original_response(
                        embed=discord.Embed(
                            title="The mine crumbles down!",
                            description=f"As the {self.mine_name} crumbles down, you are forced to leave.",
                            colour=discord.Colour.from_rgb(139, 69, 19),
                        ),
                        view=None,
                    )

            if self.mined_ores == len(self.ore_positions):
                await interaction.edit_original_response(
                    embed=discord.Embed(
                        title="You have mined all the ores!",
                        description="You have mined all the ores in the mine, you are forced to leave.",
                        colour=discord.Colour.from_rgb(139, 69, 19),
                    ),
                    view=None,
                )

                user_data = await DataManager.get_user_data(interaction.user.id)
                mining_xp = user_data["mining_xp"]
                if mining_xp == None:
                    mining_xp = 0

                await DataManager.edit_user_data(
                    interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                )

    @discord.ui.button(style=discord.ButtonStyle.gray, label="⠀", row=2)
    async def twelfth(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer()
        self.twelfth.disabled = True

        if not self.closed:
            if 12 in self.ore_positions:
                self.mined_ores += 1
                self.twelfth.label = None
                self.twelfth.emoji = self.ores[self.ore_positions[12]]["emoji"]

                xp = self.ores[self.ore_positions[12]]["xp"]
                self.gained_xp += xp

                ore = self.ore_positions[12]
                if ore in self.mined_items:
                    self.mined_items[ore] += 1
                else:
                    self.mined_items[ore] = 1

            await interaction.edit_original_response(view=self)
            if not self.button_clicked:
                self.button_clicked = True

                await asyncio.sleep(17)
                self.closed = True

                if self.mined_ores == len(self.ore_positions):
                    pass
                else:
                    user_data = await DataManager.get_user_data(interaction.user.id)
                    mining_xp = user_data["mining_xp"]
                    if mining_xp == None:
                        mining_xp = 0

                    await DataManager.edit_user_data(
                        interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                    )

                    for ore, quantity in self.mined_items.items():
                        await DataManager.edit_user_inventory(
                            interaction.user.id, ore, quantity
                        )

                    return await interaction.edit_original_response(
                        embed=discord.Embed(
                            title="The mine crumbles down!",
                            description=f"As the {self.mine_name} crumbles down, you are forced to leave.",
                            colour=discord.Colour.from_rgb(139, 69, 19),
                        ),
                        view=None,
                    )

            if self.mined_ores == len(self.ore_positions):
                await interaction.edit_original_response(
                    embed=discord.Embed(
                        title="You have mined all the ores!",
                        description="You have mined all the ores in the mine, you are forced to leave.",
                        colour=discord.Colour.from_rgb(139, 69, 19),
                    ),
                    view=None,
                )

                user_data = await DataManager.get_user_data(interaction.user.id)
                mining_xp = user_data["mining_xp"]
                if mining_xp == None:
                    mining_xp = 0

                await DataManager.edit_user_data(
                    interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                )

    @discord.ui.button(style=discord.ButtonStyle.gray, label="⠀", row=2)
    async def thirteenth(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer()
        self.thirteenth.disabled = True

        if not self.closed:
            if 13 in self.ore_positions:
                self.mined_ores += 1
                self.thirteenth.label = None
                self.thirteenth.emoji = self.ores[self.ore_positions[13]]["emoji"]

                xp = self.ores[self.ore_positions[13]]["xp"]
                self.gained_xp += xp

                ore = self.ore_positions[13]
                if ore in self.mined_items:
                    self.mined_items[ore] += 1
                else:
                    self.mined_items[ore] = 1

            await interaction.edit_original_response(view=self)
            if not self.button_clicked:
                self.button_clicked = True

                await asyncio.sleep(17)
                self.closed = True

                if self.mined_ores == len(self.ore_positions):
                    pass
                else:
                    user_data = await DataManager.get_user_data(interaction.user.id)
                    mining_xp = user_data["mining_xp"]
                    if mining_xp == None:
                        mining_xp = 0

                    await DataManager.edit_user_data(
                        interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                    )

                    for ore, quantity in self.mined_items.items():
                        await DataManager.edit_user_inventory(
                            interaction.user.id, ore, quantity
                        )

                    return await interaction.edit_original_response(
                        embed=discord.Embed(
                            title="The mine crumbles down!",
                            description=f"As the {self.mine_name} crumbles down, you are forced to leave.",
                            colour=discord.Colour.from_rgb(139, 69, 19),
                        ),
                        view=None,
                    )

            if self.mined_ores == len(self.ore_positions):
                await interaction.edit_original_response(
                    embed=discord.Embed(
                        title="You have mined all the ores!",
                        description="You have mined all the ores in the mine, you are forced to leave.",
                        colour=discord.Colour.from_rgb(139, 69, 19),
                    ),
                    view=None,
                )

                user_data = await DataManager.get_user_data(interaction.user.id)
                mining_xp = user_data["mining_xp"]
                if mining_xp == None:
                    mining_xp = 0

                await DataManager.edit_user_data(
                    interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                )

    @discord.ui.button(style=discord.ButtonStyle.gray, label="⠀", row=2)
    async def fourteenth(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer()
        self.fourteenth.disabled = True

        if not self.closed:
            if 14 in self.ore_positions:
                self.mined_ores += 1
                self.fourteenth.label = None
                self.fourteenth.emoji = self.ores[self.ore_positions[14]]["emoji"]

                xp = self.ores[self.ore_positions[14]]["xp"]
                self.gained_xp += xp

                ore = self.ore_positions[14]
                if ore in self.mined_items:
                    self.mined_items[ore] += 1
                else:
                    self.mined_items[ore] = 1

            await interaction.edit_original_response(view=self)
            if not self.button_clicked:
                self.button_clicked = True

                await asyncio.sleep(17)
                self.closed = True

                if self.mined_ores == len(self.ore_positions):
                    pass
                else:
                    user_data = await DataManager.get_user_data(interaction.user.id)
                    mining_xp = user_data["mining_xp"]
                    if mining_xp == None:
                        mining_xp = 0

                    await DataManager.edit_user_data(
                        interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                    )

                    for ore, quantity in self.mined_items.items():
                        await DataManager.edit_user_inventory(
                            interaction.user.id, ore, quantity
                        )

                    return await interaction.edit_original_response(
                        embed=discord.Embed(
                            title="The mine crumbles down!",
                            description=f"As the {self.mine_name} crumbles down, you are forced to leave.",
                            colour=discord.Colour.from_rgb(139, 69, 19),
                        ),
                        view=None,
                    )

            if self.mined_ores == len(self.ore_positions):
                await interaction.edit_original_response(
                    embed=discord.Embed(
                        title="You have mined all the ores!",
                        description="You have mined all the ores in the mine, you are forced to leave.",
                        colour=discord.Colour.from_rgb(139, 69, 19),
                    ),
                    view=None,
                )

                user_data = await DataManager.get_user_data(interaction.user.id)
                mining_xp = user_data["mining_xp"]
                if mining_xp == None:
                    mining_xp = 0

                await DataManager.edit_user_data(
                    interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                )

    @discord.ui.button(style=discord.ButtonStyle.gray, label="⠀", row=2)
    async def fifteenth(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer()
        self.fifteenth.disabled = True

        if not self.closed:
            if 15 in self.ore_positions:
                self.mined_ores += 1
                self.fifteenth.label = None
                self.fifteenth.emoji = self.ores[self.ore_positions[15]]["emoji"]

                xp = self.ores[self.ore_positions[15]]["xp"]
                self.gained_xp += xp

                ore = self.ore_positions[15]
                if ore in self.mined_items:
                    self.mined_items[ore] += 1
                else:
                    self.mined_items[ore] = 1

            await interaction.edit_original_response(view=self)
            if not self.button_clicked:
                self.button_clicked = True

                await asyncio.sleep(17)
                self.closed = True

                if self.mined_ores == len(self.ore_positions):
                    pass
                else:
                    user_data = await DataManager.get_user_data(interaction.user.id)
                    mining_xp = user_data["mining_xp"]
                    if mining_xp == None:
                        mining_xp = 0

                    await DataManager.edit_user_data(
                        interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                    )

                    for ore, quantity in self.mined_items.items():
                        await DataManager.edit_user_inventory(
                            interaction.user.id, ore, quantity
                        )

                    return await interaction.edit_original_response(
                        embed=discord.Embed(
                            title="The mine crumbles down!",
                            description=f"As the {self.mine_name} crumbles down, you are forced to leave.",
                            colour=discord.Colour.from_rgb(139, 69, 19),
                        ),
                        view=None,
                    )

            if self.mined_ores == len(self.ore_positions):
                await interaction.edit_original_response(
                    embed=discord.Embed(
                        title="You have mined all the ores!",
                        description="You have mined all the ores in the mine, you are forced to leave.",
                        colour=discord.Colour.from_rgb(139, 69, 19),
                    ),
                    view=None,
                )

                user_data = await DataManager.get_user_data(interaction.user.id)
                mining_xp = user_data["mining_xp"]
                if mining_xp == None:
                    mining_xp = 0

                await DataManager.edit_user_data(
                    interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                )

    @discord.ui.button(style=discord.ButtonStyle.gray, label="⠀", row=3)
    async def sixteenth(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer()
        self.sixteenth.disabled = True

        if not self.closed:
            if 16 in self.ore_positions:
                self.mined_ores += 1
                self.sixteenth.label = None
                self.sixteenth.emoji = self.ores[self.ore_positions[16]]["emoji"]

                xp = self.ores[self.ore_positions[16]]["xp"]
                self.gained_xp += xp

                ore = self.ore_positions[16]
                if ore in self.mined_items:
                    self.mined_items[ore] += 1
                else:
                    self.mined_items[ore] = 1

            await interaction.edit_original_response(view=self)
            if not self.button_clicked:
                self.button_clicked = True

                await asyncio.sleep(17)
                self.closed = True

                if self.mined_ores == len(self.ore_positions):
                    pass
                else:
                    user_data = await DataManager.get_user_data(interaction.user.id)
                    mining_xp = user_data["mining_xp"]
                    if mining_xp == None:
                        mining_xp = 0

                    await DataManager.edit_user_data(
                        interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                    )

                    for ore, quantity in self.mined_items.items():
                        await DataManager.edit_user_inventory(
                            interaction.user.id, ore, quantity
                        )

                    return await interaction.edit_original_response(
                        embed=discord.Embed(
                            title="The mine crumbles down!",
                            description=f"As the {self.mine_name} crumbles down, you are forced to leave.",
                            colour=discord.Colour.from_rgb(139, 69, 19),
                        ),
                        view=None,
                    )

            if self.mined_ores == len(self.ore_positions):
                await interaction.edit_original_response(
                    embed=discord.Embed(
                        title="You have mined all the ores!",
                        description="You have mined all the ores in the mine, you are forced to leave.",
                        colour=discord.Colour.from_rgb(139, 69, 19),
                    ),
                    view=None,
                )

                user_data = await DataManager.get_user_data(interaction.user.id)
                mining_xp = user_data["mining_xp"]
                if mining_xp == None:
                    mining_xp = 0

                await DataManager.edit_user_data(
                    interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                )

    @discord.ui.button(style=discord.ButtonStyle.gray, label="⠀", row=3)
    async def seventeenth(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer()
        self.seventeenth.disabled = True

        if not self.closed:
            if 17 in self.ore_positions:
                self.mined_ores += 1
                self.seventeenth.label = None
                self.seventeenth.emoji = self.ores[self.ore_positions[17]]["emoji"]

                xp = self.ores[self.ore_positions[17]]["xp"]
                self.gained_xp += xp

                ore = self.ore_positions[17]
                if ore in self.mined_items:
                    self.mined_items[ore] += 1
                else:
                    self.mined_items[ore] = 1

            await interaction.edit_original_response(view=self)
            if not self.button_clicked:
                self.button_clicked = True

                await asyncio.sleep(17)
                self.closed = True

                if self.mined_ores == len(self.ore_positions):
                    pass
                else:
                    user_data = await DataManager.get_user_data(interaction.user.id)
                    mining_xp = user_data["mining_xp"]
                    if mining_xp == None:
                        mining_xp = 0

                    await DataManager.edit_user_data(
                        interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                    )

                    for ore, quantity in self.mined_items.items():
                        await DataManager.edit_user_inventory(
                            interaction.user.id, ore, quantity
                        )

                    return await interaction.edit_original_response(
                        embed=discord.Embed(
                            title="The mine crumbles down!",
                            description=f"As the {self.mine_name} crumbles down, you are forced to leave.",
                            colour=discord.Colour.from_rgb(139, 69, 19),
                        ),
                        view=None,
                    )

            if self.mined_ores == len(self.ore_positions):
                await interaction.edit_original_response(
                    embed=discord.Embed(
                        title="You have mined all the ores!",
                        description="You have mined all the ores in the mine, you are forced to leave.",
                        colour=discord.Colour.from_rgb(139, 69, 19),
                    ),
                    view=None,
                )

                user_data = await DataManager.get_user_data(interaction.user.id)
                mining_xp = user_data["mining_xp"]
                if mining_xp == None:
                    mining_xp = 0

                await DataManager.edit_user_data(
                    interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                )

    @discord.ui.button(style=discord.ButtonStyle.gray, label="⠀", row=3)
    async def eightheenth(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer()
        self.eightheenth.disabled = True

        if not self.closed:
            if 18 in self.ore_positions:
                self.mined_ores += 1
                self.eightheenth.label = None
                self.eightheenth.emoji = self.ores[self.ore_positions[18]]["emoji"]

                xp = self.ores[self.ore_positions[18]]["xp"]
                self.gained_xp += xp

                ore = self.ore_positions[18]
                if ore in self.mined_items:
                    self.mined_items[ore] += 1
                else:
                    self.mined_items[ore] = 1

            await interaction.edit_original_response(view=self)
            if not self.button_clicked:
                self.button_clicked = True

                await asyncio.sleep(17)
                self.closed = True

                if self.mined_ores == len(self.ore_positions):
                    pass
                else:
                    user_data = await DataManager.get_user_data(interaction.user.id)
                    mining_xp = user_data["mining_xp"]
                    if mining_xp == None:
                        mining_xp = 0

                    await DataManager.edit_user_data(
                        interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                    )

                    for ore, quantity in self.mined_items.items():
                        await DataManager.edit_user_inventory(
                            interaction.user.id, ore, quantity
                        )

                    return await interaction.edit_original_response(
                        embed=discord.Embed(
                            title="The mine crumbles down!",
                            description=f"As the {self.mine_name} crumbles down, you are forced to leave.",
                            colour=discord.Colour.from_rgb(139, 69, 19),
                        ),
                        view=None,
                    )

            if self.mined_ores == len(self.ore_positions):
                await interaction.edit_original_response(
                    embed=discord.Embed(
                        title="You have mined all the ores!",
                        description="You have mined all the ores in the mine, you are forced to leave.",
                        colour=discord.Colour.from_rgb(139, 69, 19),
                    ),
                    view=None,
                )

                user_data = await DataManager.get_user_data(interaction.user.id)
                mining_xp = user_data["mining_xp"]
                if mining_xp == None:
                    mining_xp = 0

                await DataManager.edit_user_data(
                    interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                )

    @discord.ui.button(style=discord.ButtonStyle.gray, label="⠀", row=3)
    async def nineteenth(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer()
        self.nineteenth.disabled = True

        if not self.closed:
            if 19 in self.ore_positions:
                self.mined_ores += 1
                self.nineteenth.label = None
                self.nineteenth.emoji = self.ores[self.ore_positions[19]]["emoji"]

                xp = self.ores[self.ore_positions[19]]["xp"]
                self.gained_xp += xp

                ore = self.ore_positions[19]
                if ore in self.mined_items:
                    self.mined_items[ore] += 1
                else:
                    self.mined_items[ore] = 1

            await interaction.edit_original_response(view=self)
            if not self.button_clicked:
                self.button_clicked = True

                await asyncio.sleep(17)
                self.closed = True

                if self.mined_ores == len(self.ore_positions):
                    pass
                else:
                    user_data = await DataManager.get_user_data(interaction.user.id)
                    mining_xp = user_data["mining_xp"]
                    if mining_xp == None:
                        mining_xp = 0

                    await DataManager.edit_user_data(
                        interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                    )

                    return await interaction.edit_original_response(
                        embed=discord.Embed(
                            title="The mine crumbles down!",
                            description=f"As the {self.mine_name} crumbles down, you are forced to leave.",
                            colour=discord.Colour.from_rgb(139, 69, 19),
                        ),
                        view=None,
                    )

            if self.mined_ores == len(self.ore_positions):
                await interaction.edit_original_response(
                    embed=discord.Embed(
                        title="You have mined all the ores!",
                        description="You have mined all the ores in the mine, you are forced to leave.",
                        colour=discord.Colour.from_rgb(139, 69, 19),
                    ),
                    view=None,
                )

                user_data = await DataManager.get_user_data(interaction.user.id)
                mining_xp = user_data["mining_xp"]
                if mining_xp == None:
                    mining_xp = 0

                await DataManager.edit_user_data(
                    interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                )

    @discord.ui.button(style=discord.ButtonStyle.gray, label="⠀", row=3)
    async def twentieth(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer()
        self.twentieth.disabled = True

        if not self.closed:
            if 20 in self.ore_positions:
                self.mined_ores += 1
                self.twentieth.label = None
                self.twentieth.emoji = self.ores[self.ore_positions[20]]["emoji"]

                xp = self.ores[self.ore_positions[20]]["xp"]
                self.gained_xp += xp

                ore = self.ore_positions[20]
                if ore in self.mined_items:
                    self.mined_items[ore] += 1
                else:
                    self.mined_items[ore] = 1

            await interaction.edit_original_response(view=self)
            if not self.button_clicked:
                self.button_clicked = True

                await asyncio.sleep(17)
                self.closed = True

                if self.mined_ores == len(self.ore_positions):
                    pass
                else:
                    user_data = await DataManager.get_user_data(interaction.user.id)
                    mining_xp = user_data["mining_xp"]
                    if mining_xp == None:
                        mining_xp = 0

                    await DataManager.edit_user_data(
                        interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                    )

                    for ore, quantity in self.mined_items.items():
                        await DataManager.edit_user_inventory(
                            interaction.user.id, ore, quantity
                        )

                    return await interaction.edit_original_response(
                        embed=discord.Embed(
                            title="The mine crumbles down!",
                            description=f"As the {self.mine_name} crumbles down, you are forced to leave.",
                            colour=discord.Colour.from_rgb(139, 69, 19),
                        ),
                        view=None,
                    )

            if self.mined_ores == len(self.ore_positions):
                await interaction.edit_original_response(
                    embed=discord.Embed(
                        title="You have mined all the ores!",
                        description="You have mined all the ores in the mine, you are forced to leave.",
                        colour=discord.Colour.from_rgb(139, 69, 19),
                    ),
                    view=None,
                )

                user_data = await DataManager.get_user_data(interaction.user.id)
                mining_xp = user_data["mining_xp"]
                if mining_xp == None:
                    mining_xp = 0

                await DataManager.edit_user_data(
                    interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                )

    @discord.ui.button(style=discord.ButtonStyle.gray, label="⠀", row=4)
    async def twentyfirst(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer()
        self.twentyfirst.disabled = True

        if not self.closed:
            if 21 in self.ore_positions:
                self.mined_ores += 1
                self.twentyfirst.label = None
                self.twentyfirst.emoji = self.ores[self.ore_positions[21]]["emoji"]

                xp = self.ores[self.ore_positions[21]]["xp"]
                self.gained_xp += xp

                ore = self.ore_positions[21]
                if ore in self.mined_items:
                    self.mined_items[ore] += 1
                else:
                    self.mined_items[ore] = 1

            await interaction.edit_original_response(view=self)
            if not self.button_clicked:
                self.button_clicked = True

                await asyncio.sleep(17)
                self.closed = True

                if self.mined_ores == len(self.ore_positions):
                    pass
                else:
                    user_data = await DataManager.get_user_data(interaction.user.id)
                    mining_xp = user_data["mining_xp"]
                    if mining_xp == None:
                        mining_xp = 0

                    await DataManager.edit_user_data(
                        interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                    )

                    for ore, quantity in self.mined_items.items():
                        await DataManager.edit_user_inventory(
                            interaction.user.id, ore, quantity
                        )

                    return await interaction.edit_original_response(
                        embed=discord.Embed(
                            title="The mine crumbles down!",
                            description=f"As the {self.mine_name} crumbles down, you are forced to leave.",
                            colour=discord.Colour.from_rgb(139, 69, 19),
                        ),
                        view=None,
                    )

            if self.mined_ores == len(self.ore_positions):
                await interaction.edit_original_response(
                    embed=discord.Embed(
                        title="You have mined all the ores!",
                        description="You have mined all the ores in the mine, you are forced to leave.",
                        colour=discord.Colour.from_rgb(139, 69, 19),
                    ),
                    view=None,
                )

                user_data = await DataManager.get_user_data(interaction.user.id)
                mining_xp = user_data["mining_xp"]
                if mining_xp == None:
                    mining_xp = 0

                await DataManager.edit_user_data(
                    interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                )

    @discord.ui.button(style=discord.ButtonStyle.gray, label="⠀", row=4)
    async def twentysecond(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer()
        self.twentysecond.disabled = True

        if not self.closed:
            if 22 in self.ore_positions:
                self.mined_ores += 1
                self.twentysecond.label = None
                self.twentysecond.emoji = self.ores[self.ore_positions[22]]["emoji"]

                xp = self.ores[self.ore_positions[22]]["xp"]
                self.gained_xp += xp

                ore = self.ore_positions[22]
                if ore in self.mined_items:
                    self.mined_items[ore] += 1
                else:
                    self.mined_items[ore] = 1

            await interaction.edit_original_response(view=self)
            if not self.button_clicked:
                self.button_clicked = True

                await asyncio.sleep(17)
                self.closed = True

                if self.mined_ores == len(self.ore_positions):
                    pass
                else:
                    user_data = await DataManager.get_user_data(interaction.user.id)
                    mining_xp = user_data["mining_xp"]
                    if mining_xp == None:
                        mining_xp = 0

                    await DataManager.edit_user_data(
                        interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                    )

                    for ore, quantity in self.mined_items.items():
                        await DataManager.edit_user_inventory(
                            interaction.user.id, ore, quantity
                        )

                    return await interaction.edit_original_response(
                        embed=discord.Embed(
                            title="The mine crumbles down!",
                            description=f"As the {self.mine_name} crumbles down, you are forced to leave.",
                            colour=discord.Colour.from_rgb(139, 69, 19),
                        ),
                        view=None,
                    )

            if self.mined_ores == len(self.ore_positions):
                await interaction.edit_original_response(
                    embed=discord.Embed(
                        title="You have mined all the ores!",
                        description="You have mined all the ores in the mine, you are forced to leave.",
                        colour=discord.Colour.from_rgb(139, 69, 19),
                    ),
                    view=None,
                )

                user_data = await DataManager.get_user_data(interaction.user.id)
                mining_xp = user_data["mining_xp"]
                if mining_xp == None:
                    mining_xp = 0

                await DataManager.edit_user_data(
                    interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                )

                for ore, quantity in self.mined_items.items():
                    await DataManager.edit_user_inventory(
                        interaction.user.id, ore, quantity
                    )

    @discord.ui.button(style=discord.ButtonStyle.gray, label="⠀", row=4)
    async def twentythird(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer()
        self.twentythird.disabled = True

        if not self.closed:
            if 23 in self.ore_positions:
                self.mined_ores += 1
                self.twentythird.label = None
                self.twentythird.emoji = self.ores[self.ore_positions[23]]["emoji"]

                xp = self.ores[self.ore_positions[23]]["xp"]
                self.gained_xp += xp

                ore = self.ore_positions[23]
                if ore in self.mined_items:
                    self.mined_items[ore] += 1
                else:
                    self.mined_items[ore] = 1

            await interaction.edit_original_response(view=self)
            if not self.button_clicked:
                self.button_clicked = True

                await asyncio.sleep(17)
                self.closed = True

                if self.mined_ores == len(self.ore_positions):
                    pass
                else:
                    user_data = await DataManager.get_user_data(interaction.user.id)
                    mining_xp = user_data["mining_xp"]
                    if mining_xp == None:
                        mining_xp = 0

                    await DataManager.edit_user_data(
                        interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                    )

                    for ore, quantity in self.mined_items.items():
                        await DataManager.edit_user_inventory(
                            interaction.user.id, ore, quantity
                        )

                    return await interaction.edit_original_response(
                        embed=discord.Embed(
                            title="The mine crumbles down!",
                            description=f"As the {self.mine_name} crumbles down, you are forced to leave.",
                            colour=discord.Colour.from_rgb(139, 69, 19),
                        ),
                        view=None,
                    )

            if self.mined_ores == len(self.ore_positions):
                await interaction.edit_original_response(
                    embed=discord.Embed(
                        title="You have mined all the ores!",
                        description="You have mined all the ores in the mine, you are forced to leave.",
                        colour=discord.Colour.from_rgb(139, 69, 19),
                    ),
                    view=None,
                )

                user_data = await DataManager.get_user_data(interaction.user.id)
                mining_xp = user_data["mining_xp"]
                if mining_xp == None:
                    mining_xp = 0

                await DataManager.edit_user_data(
                    interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                )

    @discord.ui.button(style=discord.ButtonStyle.gray, label="⠀", row=4)
    async def twentyfourth(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer()
        self.twentyfourth.disabled = True

        if not self.closed:
            if 24 in self.ore_positions:
                self.mined_ores += 1
                self.twentyfourth.label = None
                self.twentyfourth.emoji = self.ores[self.ore_positions[24]]["emoji"]

                xp = self.ores[self.ore_positions[24]]["xp"]
                self.gained_xp += xp

                ore = self.ore_positions[24]
                if ore in self.mined_items:
                    self.mined_items[ore] += 1
                else:
                    self.mined_items[ore] = 1

            await interaction.edit_original_response(view=self)
            if not self.button_clicked:
                self.button_clicked = True

                await asyncio.sleep(17)
                self.closed = True

                if self.mined_ores == len(self.ore_positions):
                    pass
                else:
                    user_data = await DataManager.get_user_data(interaction.user.id)
                    mining_xp = user_data["mining_xp"]
                    if mining_xp == None:
                        mining_xp = 0

                    await DataManager.edit_user_data(
                        interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                    )

                    for ore, quantity in self.mined_items.items():
                        await DataManager.edit_user_inventory(
                            interaction.user.id, ore, quantity
                        )

                    return await interaction.edit_original_response(
                        embed=discord.Embed(
                            title="The mine crumbles down!",
                            description=f"As the {self.mine_name} crumbles down, you are forced to leave.",
                            colour=discord.Colour.from_rgb(139, 69, 19),
                        ),
                        view=None,
                    )

            if self.mined_ores == len(self.ore_positions):
                await interaction.edit_original_response(
                    embed=discord.Embed(
                        title="You have mined all the ores!",
                        description="You have mined all the ores in the mine, you are forced to leave.",
                        colour=discord.Colour.from_rgb(139, 69, 19),
                    ),
                    view=None,
                )

                user_data = await DataManager.get_user_data(interaction.user.id)
                mining_xp = user_data["mining_xp"]
                if mining_xp == None:
                    mining_xp = 0

                await DataManager.edit_user_data(
                    interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                )

    @discord.ui.button(style=discord.ButtonStyle.gray, label="⠀", row=4)
    async def twentyfifth(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer()
        self.twentyfifth.disabled = True

        if not self.closed:
            if 25 in self.ore_positions:
                self.mined_ores += 1
                self.twentyfifth.label = None
                self.twentyfifth.emoji = self.ores[self.ore_positions[25]]["emoji"]

                xp = self.ores[self.ore_positions[25]]["xp"]
                self.gained_xp += xp

                ore = self.ore_positions[25]
                if ore in self.mined_items:
                    self.mined_items[ore] += 1
                else:
                    self.mined_items[ore] = 1

            await interaction.edit_original_response(view=self)
            if not self.button_clicked:
                self.button_clicked = True

                await asyncio.sleep(17)
                self.closed = True

                if self.mined_ores == len(self.ore_positions):
                    pass
                else:
                    user_data = await DataManager.get_user_data(interaction.user.id)
                    mining_xp = user_data["mining_xp"]
                    if mining_xp == None:
                        mining_xp = 0

                    await DataManager.edit_user_data(
                        interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                    )

                    for ore, quantity in self.mined_items.items():
                        await DataManager.edit_user_inventory(
                            interaction.user.id, ore, quantity
                        )

                    return await interaction.edit_original_response(
                        embed=discord.Embed(
                            title="The mine crumbles down!",
                            description=f"As the {self.mine_name} crumbles down, you are forced to leave.",
                            colour=discord.Colour.from_rgb(139, 69, 19),
                        ),
                        view=None,
                    )

            if self.mined_ores == len(self.ore_positions):
                await interaction.edit_original_response(
                    embed=discord.Embed(
                        title="You have mined all the ores!",
                        description="You have mined all the ores in the mine, you are forced to leave.",
                        colour=discord.Colour.from_rgb(139, 69, 19),
                    ),
                    view=None,
                )

                user_data = await DataManager.get_user_data(interaction.user.id)
                mining_xp = user_data["mining_xp"]
                if mining_xp == None:
                    mining_xp = 0

                await DataManager.edit_user_data(
                    interaction.user.id, "mining_xp", mining_xp + self.gained_xp
                )
                for ore, quantity in self.mined_items.items():
                    await DataManager.edit_user_inventory(
                        interaction.user.id, ore, quantity
                    )


class choose_mine(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=60)
        self.bot = bot
        self.response: discord.Message = None

    async def on_timeout(self) -> None:
        return await self.response.delete()

    @discord.ui.button(
        style=discord.ButtonStyle.green,
        row=0,
        label="Coal Mine",
        emoji="<:coal:1207769912597159976>",
    )
    async def coal(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = mining_buttons(self.bot, "coal mine")
        await interaction.response.edit_message(
            embed=discord.Embed(
                description="You have entered the coal mine, here you can find mostly coal, but maybe some iron as well.",
                colour=discord.Colour.from_rgb(139, 69, 19),
            ),
            attachments=[],
            view=view,
        )
        view.response = await interaction.original_response()

    @discord.ui.button(
        style=discord.ButtonStyle.green,
        row=0,
        label="Iron Mine",
        emoji="<:iron:1207771688868253696>",
    )
    async def iron(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await find_user_level(interaction.user.id) < 10:
            return await interaction.response.send_message(
                f"You need to be level 10 to enter the iron mine! Your current level is {await find_user_level(interaction.user.id)}",
                ephemeral=True,
            )

        else:
            view = mining_buttons(self.bot, "iron mine")
            await interaction.response.edit_message(
                embed=discord.Embed(
                    description="You have entered the iron mine, here you can find mostly iron, but maybe some coal as well.",
                    colour=discord.Colour.from_rgb(139, 69, 19),
                ),
                attachments=[],
                view=view,
            )
            view.response = await interaction.original_response()

    @discord.ui.button(
        style=discord.ButtonStyle.green,
        row=0,
        label="Gold Mine",
        emoji="<:gold:1207771927490461748>",
    )
    async def gold(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await find_user_level(interaction.user.id) < 26:
            return await interaction.response.send_message(
                f"You need to be level 25 to enter the gold mine! Your current level is {await find_user_level(interaction.user.id)}",
                ephemeral=True,
            )

        else:
            view = mining_buttons(self.bot, "gold mine")
            await interaction.response.edit_message(
                embed=discord.Embed(
                    description="You have entered the gold mine, here you can find mostly gold, but maybe some iron as well.",
                    colour=discord.Colour.from_rgb(139, 69, 19),
                ),
                attachments=[],
                view=view,
            )
            view.response = await interaction.original_response()

    @discord.ui.button(
        style=discord.ButtonStyle.green,
        row=0,
        label="Abyss Mine",
        emoji="<:abyss:1207772268160352367>",
    )
    async def abyss(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await find_user_level(interaction.user.id) < 35:
            return await interaction.response.send_message(
                f"You need to be level 40 to enter the abyss mine! Your current level is {await find_user_level(interaction.user.id)}",
                ephemeral=True,
            )

        else:
            view = mining_buttons(self.bot, "abyss mine")
            await interaction.response.edit_message(
                embed=discord.Embed(
                    description="You have entered the abyss mine, here you can find mostly abyssalite, but maybe some gold as well.",
                    colour=discord.Colour.from_rgb(139, 69, 19),
                ),
                attachments=[],
                view=view,
            )
            view.response = await interaction.original_response()

    @discord.ui.button(
        style=discord.ButtonStyle.green,
        row=0,
        label="Drunkite Mine",
        emoji="<:drunkite:1207779744528076860>",
    )
    async def drunkite(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if await find_user_level(interaction.user.id) < 50:
            return await interaction.response.send_message(
                f"You need to be level 50 to enter the drunkite mine! Your current level is {await find_user_level(interaction.user.id)}",
                ephemeral=True,
            )

        else:
            view = mining_buttons(self.bot, "drunkite mine")
            await interaction.response.edit_message(
                embed=discord.Embed(
                    description="You have entered the drunkite mine, here you can find mostly drunkite, but maybe some abyssalite as well.",
                    colour=discord.Colour.from_rgb(139, 69, 19),
                ),
                attachments=[],
                view=view,
            )
            view.response = await interaction.original_response()


class mine(commands.GroupCog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @app_commands.command(name="start", description="Mine for resources")
    async def mine_start(self, interaction: discord.Interaction):
        if await cooldown_check(
            interaction.user.id,
            "<:white_cross:1096791282023669860> You already went mining",
            "mine",
            1800
        ):
            f = discord.File(
                "data/mine/mining_assets/mine_background.jpg", filename="mining.jpg"
            )
            view = choose_mine(self.bot)
            await interaction.response.send_message(
                file=f,
                embed=discord.Embed(
                    description="Welcome to the mines, here you are able to mine for various resources, and later smelt them down to craft various items with them.",
                    colour=discord.Colour.from_rgb(139, 69, 19),
                ).set_image(url="attachment://mining.jpg"),
                view=view,
                ephemeral=True,
            )
            view.response = await interaction.original_response()

    @app_commands.command(name="level", description="Check your mining level")
    @app_commands.checks.cooldown(1, 60, key=lambda i: (i.user.id))
    async def mine_level(self, interaction: discord.Interaction):
        level = await find_user_level(interaction.user.id)
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Mining Level",
                description=f"Your current mining level is {level}",
                colour=discord.Colour.from_rgb(139, 69, 19),
            ).set_thumbnail(url=interaction.user.avatar.url),
            ephemeral=True,
        )


async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(mine(bot))
