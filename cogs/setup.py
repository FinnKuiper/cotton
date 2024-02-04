from discord.ext import commands
from dotenv import load_dotenv
import os
from pymongo_get_database import get_database

load_dotenv()
guild_id = int(os.getenv("GUILD_ID"))


class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="setup", with_app_command=True, description="Setup the bot"
    )
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx):
        guild = ctx.guild
        # get database
        dbname = get_database()
        collection_name = dbname["guild"]

        # check if guild is already in the system
        guild_data = collection_name.find_one({"guild_id": guild.id})
        if guild_data:
            await ctx.send(
                f"{guild.name} is already in the system, if you haven't set the update channel yet, use the command `setUpdateChannel`, by default the prefix is set to `!`, you can check this by using the commmand `setprefix`"
            )
            return

        # create item
        item = {
            "name": guild.name,
            "guild_id": guild.id,
            "owner": guild.owner,
            "update_channel": None,
            "welcome_channel": None,
            "leveling": False,
            "prefix": "!",
            "expiry_date": None,
        }

        # insert item
        collection_name.insert_one(item)
        await ctx.send(
            f"Added {guild.name} to cotton, by default the prefix is set to `!`, you can check this by using the commmand `setprefix`, other settings can be found with the command `guildsettings`!"
        )

    @commands.Cog.listener()
    async def on_ready(self):
        print("Setup is ready")


async def setup(bot):
    await bot.add_cog(Setup(bot))
