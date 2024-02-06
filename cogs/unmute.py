from discord.ext import commands
from dotenv import load_dotenv
import discord
import os

load_dotenv()
guild_id = int(os.getenv("GUILD_ID"))


class UnMute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="unmute", with_app_command=True, description="Unmute a user"
    )
    async def unMute(self, ctx, member: discord.Member, *, reason=None):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            return await ctx.send("The user is not muted")
        await member.remove_roles(role)
        await ctx.send(f"Unmuted {member.mention}")


async def setup(bot):
    await bot.add_cog(UnMute(bot))
