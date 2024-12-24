from .slowmode import slowmode

class Server_Management(slowmode):
    """All commands that are related to the server management"""

async def setup(bot):
    await bot.add_cog(Server_Management(bot))