from .ticket_system import ticket_system

class ticket(ticket_system):
    """All commands and functions related to the ticketing system"""

async def setup(bot):
    await bot.add_cog(ticket(bot))