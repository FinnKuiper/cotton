from discord.ext import commands
from dotenv import load_dotenv
from pymongo_get_database import get_database
import os

load_dotenv()
guild_id = int(os.getenv("GUILD_ID"))


class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="level", with_app_command=True, description="Get your level in the guild"
    )
    async def level(self, ctx):
        guild_id = ctx.guild.id
        # get database
        dbname = get_database()
        collection_name = dbname["leveling"]

        # check if leveling is enabled
        guild = dbname["guild"].find_one({"guild_id": guild_id})
        leveling = guild["leveling"] if guild else False
        if not leveling:
            return await ctx.send("Leveling is not enabled in this guild!")

        # get user from the correct guild
        user = collection_name.find_one(
            {"guild_id": guild_id, "user_id": ctx.author.id}
        )
        # if user is not in the database add them
        if not user:
            user = {
                "name": ctx.author.name,
                "guild_id": ctx.guild.id,
                "user_id": ctx.author.id,
                "level": 1,
                "xp": 0,
                "xp_to_level": 100,
                "expiry_date": None,
            }
            collection_name.insert_one(user)
            await ctx.send("You are not in the database. You have been added!")
        # send message with user level and xp to next level
        await ctx.send(
            f"{ctx.author.mention} is level {user['level']} and has {user['xp']} xp. They need {user['xp_to_level'] - user['xp']} xp to level up"
        )


async def setup(bot):
    await bot.add_cog(Level(bot))
