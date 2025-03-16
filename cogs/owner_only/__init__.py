from .add import add
from .reload import reload_cogs
from .skip_cooldown import skip_cooldown

class owner_only(add, reload_cogs, skip_cooldown):
    """All commands that can be used by the owner of the bot only"""

async def setup(bot):
    await bot.add_cog(owner_only)