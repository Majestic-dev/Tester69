from .ban import ban
from .kick import kick
from .timeout import timeout
from .warning_system import warning_system

class moderation(ban, kick, timeout, warning_system):
    """All commands related to moderation"""

async def setup(bot):
    await bot.add_cog(moderation)