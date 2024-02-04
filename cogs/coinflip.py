from discord.ext import commands
from dotenv import load_dotenv
import random
import os


load_dotenv()
guild_id = int(os.getenv("GUILD_ID"))


class Coinflip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="coinflip",
        with_app_command=True,
        description="Flip a coin!",
        aliases=["cf"],
    )
    async def coinflip(self, ctx):
        await ctx.send("Flipping coin...")
        coin = ["heads", "tails"]
        await ctx.send(f"It's {random.choice(coin)}")


async def setup(bot):
    await bot.add_cog(Coinflip(bot))
