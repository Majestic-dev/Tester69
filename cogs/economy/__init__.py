from .activities import activities
from .banking import banking
from .item import item
from .leaderboard import leaderboard
from .mine import mine
from .personal import personal
from .timed_claims import timed_claims

class economy(activities, banking, item, leaderboard, mine, personal, timed_claims):
    """All systems and commands related to the economy system"""

async def setup(bot):
    await bot.add_cog(economy(bot))