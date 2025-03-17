from .giveaway_looper import giveaway_looper
from .giveaway_listeners import giveaway_listeners
from .giveaway_commands import giveaway

class giveaway(giveaway_looper, giveaway_listeners, giveaway):
    """All commands and systems that are related to the giveawat system"""

async def setup(bot):
    await bot.add_cog(giveaway(bot))