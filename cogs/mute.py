from discord.ext import commands
from dotenv import load_dotenv
import discord
import asyncio
import os

load_dotenv()
guild_id = int(os.getenv("GUILD_ID"))


class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="mute", with_app_command=True, description="Mute a member"
    )
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member: discord.Member, reason=None, time: int = None):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            role = await ctx.guild.create_role(name="Muted")
            role.permissions.update(send_messages=False)
        if time:
            await member.add_roles(role)
            await ctx.send(f"Muted {member.mention} for {time} seconds")
            await asyncio.sleep(time)
            # check if the member is still muted
            if role in member.roles:
                await member.remove_roles(role)
                await ctx.send(f"Unmuted {member.mention}")
            else:
                return
        else:
            await member.add_roles(role)
            await ctx.send(f"Muted {member.mention}")


async def setup(bot):
    await bot.add_cog(Mute(bot))
