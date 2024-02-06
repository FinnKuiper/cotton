from discord.ext import commands
from dotenv import load_dotenv
from pymongo_get_database import get_database
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

        db = get_database()
        # get the collection
        collection = db["warns"]
        # get the guild
        guild = ctx.guild

        memberId = member.id

        if collection.find_one({"user_id": memberId, "guild": guild.id}):
            # if the member is in the database
            # get the kicked
            kicked = collection.find_one({"user_id": memberId, "guild": guild.id})[
                "kicked"
            ]
            if kicked:
                return
            # update the database with the new warns and reason
            collection.update_one(
                {"user_id": memberId, "guild": guild.id},
                {"$set": {"kicked": True, "reason": reason}},
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
                    "kicked": True,
                    "muted": False,
                    "reason": reason,
                }
            )


async def setup(bot):
    await bot.add_cog(Kick(bot))
