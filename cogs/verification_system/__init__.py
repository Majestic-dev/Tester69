from .verification_system import verification

class verification_system(verification):
    """All systems and commands related to the verification system"""

async def setup(bot):
    await bot.add_cog(verification_system)
