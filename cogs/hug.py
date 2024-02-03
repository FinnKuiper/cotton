import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
guild_id = int(os.getenv("GUILD_ID"))


class Hug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="hug",
        with_app_command=True,
        description="Hug some... or yourself?",
        aliases=["h"],
    )
    async def hug(self, ctx, user: discord.Member = None):
        if user:
            await ctx.send(f"{ctx.author.mention} hugged {user.mention}")
        else:
            await ctx.send(f"{ctx.author.mention} hugged themselves!")


async def setup(bot):
    await bot.add_cog(Hug(bot))
