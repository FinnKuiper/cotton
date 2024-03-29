from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
guild_id = int(os.getenv("GUILD_ID"))


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="ping", with_app_command=True, description="Get the ping of the bot"
    )
    async def ping(self, ctx):
        await ctx.send("Pong!")


async def setup(bot):
    await bot.add_cog(Ping(bot))
