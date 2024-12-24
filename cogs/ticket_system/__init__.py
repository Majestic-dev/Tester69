
class Ticket(

):
    """All commands and functions related to the ticketing system"""

async def setup(bot):
    await bot.add_cog(Ticket(bot))