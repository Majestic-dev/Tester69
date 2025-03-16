from .serverinfo import server

class server_info(server):
    """All commands related to server info"""

async def setup(bot):
    await bot.add_cog(server_info(bot))