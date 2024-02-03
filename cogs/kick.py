from discord.ext import commands
from dotenv import load_dotenv
import os
import discord

load_dotenv()
guild_id = int(os.getenv("GUILD_ID"))


class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="kick", with_app_command=True, description="kick a user"
    )
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"Kicked {member.mention}")


async def setup(bot):
    await bot.add_cog(Kick(bot))
