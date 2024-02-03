import random
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
guild_id = int(os.getenv("GUILD_ID"))


class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="roll", with_app_command=True, description="Roll a dice!", aliases=["r"]
    )
    async def coinflip(self, ctx, number_of_sides: int = 6):
        await ctx.send("Rolling dice...")
        await ctx.send(f"You rolled a {random.randint(1, number_of_sides)}")


async def setup(bot):
    await bot.add_cog(Roll(bot))
