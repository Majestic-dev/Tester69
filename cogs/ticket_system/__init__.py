from .ticket_system import ticket

class Ticket(ticket):
    """All commands and functions related to the ticketing system"""

async def setup(bot):
    await bot.add_cog(Ticket(bot))