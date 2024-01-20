from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
import discord

load_dotenv()
guild_id = int(os.getenv("GUILD_ID"))


class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="ban", with_app_command=True, description="ban a user"
    )
    @app_commands.guilds(discord.Object(id=guild_id))
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"Banned {member.mention}")


async def setup(bot):
    await bot.add_cog(Ban(bot))
