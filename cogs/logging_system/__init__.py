from .logging_commands import logging
from .logging_listeners import logging_listeners

class logging_system(logging, logging_listeners):
    """All systems related to the logging system"""

async def setup(bot):
    await bot.add_cog(logging_system)