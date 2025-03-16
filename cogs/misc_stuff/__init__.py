from .fun import fun
from .misc import misc
from .search import search
from .weather import weather

class misc_stuff(fun, misc, search, weather):
    """All commands that are related to miscallaneous stuff"""

async def setup(bot):
    await bot.add_cog(misc_stuff)