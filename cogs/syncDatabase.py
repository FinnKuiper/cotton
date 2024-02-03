from discord.ext import commands
from dotenv import load_dotenv
from pymongo_get_database import get_database
import os

load_dotenv()
guild_id = int(os.getenv("GUILD_ID"))


class SyncDatabase(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3600, commands.BucketType.guild)
    @commands.hybrid_command(
        name="syncdatabase",
        with_app_command=True,
        description="If a user isn't in the database this would add them. (cooldown of 1 hour)",
    )
    @commands.has_permissions(administrator=True)
    async def syncdatabase(self, ctx):
        # check for every user in the guild if they are in the leveling database
        # if not add them
        # get database

        await ctx.send("Getting database...")
        dbname = get_database()
        collection_name = dbname["leveling"]

        # get all users in the guild
        await ctx.send("Getting users...")
        guild = ctx.guild
        members = guild.members
        # find all users that are associated with the guild in the database
        users = collection_name.find({"guild_id": guild.id})
        # get all ids of users in the database
        users_in_database = []
        for user in users:
            users_in_database.append(user["user_id"])

        # check if the user is in the database
        await ctx.send("Checking if user is in the database...")
        for member in members:
            # if user is bot skip
            if member.bot:
                continue
            if member.id not in users_in_database:
                await ctx.send(f"Adding {member} to the database...")
                # add user to database
                user = {
                    "name": member.name,
                    "guild_id": guild.id,
                    "user_id": member.id,
                    "level": 1,
                    "xp": 0,
                    "xp_to_level": 100,
                    "expiry_date": None,
                }
                collection_name.insert_one(user)

        await ctx.send("Done! All members should be in the database now")


async def setup(bot):
    await bot.add_cog(SyncDatabase(bot))
