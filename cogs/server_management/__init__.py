from .appeal import appealing
from .blacklist import blacklist
from .role import role
from .slowmode import slowmode
from .whitelist import whitelist

class Server_Management(appealing, blacklist, role, slowmode, whitelist):
    """All commands that are related to the server management"""

async def setup(bot):
    await bot.add_cog(Server_Management(bot))