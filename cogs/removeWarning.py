from discord.ext import commands
from dotenv import load_dotenv
from pymongo_get_database import get_database
import discord
import os

load_dotenv()
guild_id = int(os.getenv("GUILD_ID"))


class RemoveWarning(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="removewarning",
        with_app_command=True,
        description="remove a warning of a user",
    )
    @commands.has_permissions(administrator=True)
    async def removeWarning(self, ctx, member: discord.Member):
        # get the database
        db = get_database()
        # get the collection
        collection = db["warns"]
        # get the guild
        guild = ctx.guild

        memberId = member.id

        if collection.find_one({"user_id": memberId, "guild": guild.id}):
            # if the member is in the database
            # get the warns
            warns = collection.find_one({"user_id": memberId, "guild": guild.id})[
                "warns"
            ]
            if warns == 0:
                return await ctx.reply("A user cannot have negative warnings :/")
            # remove a warn
            warns -= 1
            # update the database with the new warns and reason
            collection.update_one(
                {"user_id": memberId, "guild": guild.id},
                {"$set": {"warns": warns}},
            )
            # send a message
            await ctx.send(f"{member.mention} has had a warning removed")


async def setup(bot):
    await bot.add_cog(RemoveWarning(bot))
