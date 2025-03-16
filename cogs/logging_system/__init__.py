from .logging_commands import logging_cmds
from .logging_listeners import logging_listeners

class logging(logging_cmds, logging_listeners):
    """All systems related to the logging system"""

async def setup(bot):
    await bot.add_cog(logging(bot))