from discord.ext import commands
from dotenv import load_dotenv
from pymongo_get_database import get_database
from discord.ext.commands import MemberConverter
import os

load_dotenv()
guild_id = int(os.getenv("GUILD_ID"))


class Warn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="warn", with_app_command=True, description="Warn a user of their actions"
    )
    @commands.has_permissions(administrator=True)
    async def ping(self, ctx, member: MemberConverter(), *, reason=None):
        # get the database
        db = get_database()
        # get the collection
        collection = db["warns"]
        # get the guild
        guild = ctx.guild
        # get the member
        memberMention = member.mention
        memberId = member.id

        # check if the member is in the database
        if collection.find_one({"user_id": memberId, "guild": guild.id}):
            # if the member is in the database
            # get the warns
            warns = collection.find_one({"user_id": memberId, "guild": guild.id})[
                "warns"
            ]
            # add a warn
            warns += 1
            # update the database with the new warns and reason
            collection.update_one(
                {"user_id": memberId, "guild": guild.id},
                {"$set": {"warns": warns, "reason": reason}},
            )
            # send a message
            await ctx.send(f"{memberMention} has been warned")
        else:
            # if the member is not in the database
            # add the member to the database
            collection.insert_one(
                {
                    "name": member.name,
                    "user_id": memberId,
                    "guild": guild.id,
                    "warns": 1,
                    "banned": False,
                    "kicked": False,
                    "muted": False,
                    "reason": reason,
                }
            )
            # send a message
            await ctx.send(f"{memberMention} has been warned")


async def setup(bot):
    await bot.add_cog(Warn(bot))
