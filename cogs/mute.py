from discord.ext import commands
from dotenv import load_dotenv
from pymongo_get_database import get_database
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
        def setMuted():
            db = get_database()
            # get the collection
            collection = db["warns"]
            # get the guild
            guild = ctx.guild

            memberId = member.id

            if collection.find_one({"user_id": memberId, "guild": guild.id}):
                # if the member is in the database
                # get the banned
                banned = collection.find_one({"user_id": memberId, "guild": guild.id})[
                    "muted"
                ]
                if banned:
                    return
                # update the database with the new warns and reason
                collection.update_one(
                    {"user_id": memberId, "guild": guild.id},
                    {"$set": {"muted": True, "reason": reason}},
                )
            else:
                # if the member is not in the database
                # add the member to the database
                collection.insert_one(
                    {
                        "name": member.name,
                        "user_id": memberId,
                        "guild": guild.id,
                        "warns": 0,
                        "banned": False,
                        "kicked": False,
                        "muted": True,
                        "reason": reason,
                    }
                )

        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            role = await ctx.guild.create_role(name="Muted")
            role.permissions.update(send_messages=False)
        if time:
            await member.add_roles(role)
            await ctx.send(f"Muted {member.mention} for {time} seconds")
            setMuted()
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
            setMuted()


async def setup(bot):
    await bot.add_cog(Mute(bot))
