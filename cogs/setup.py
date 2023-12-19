from discord.ext import commands
from pymongo_get_database import get_database

class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setup(self, ctx):
        # make sure the user is an admin
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("You don't have the permission to use this command")
            return
        
        guild = ctx.guild
        # get database
        dbname = get_database()
        collection_name = dbname["guild"]

        # check if guild is already in the system
        guild_data = collection_name.find_one({"guild_id": guild.id})
        if guild_data:
            await ctx.send(f"{guild.name} is already in the system, if you haven't set the update channel yet, use the command `!setUpdateChannel`, by default the prefix is set to `!`, you can check this by using the commmand `!guildInfo`")
            return
        
        # create item
        item = {
            "name": guild.name,
            "guild_id": guild.id,
            "owner": guild.owner,
            "update_channel": None,
            "prefix": "!",
            "expiry_date": None
        }
        
        # insert item
        collection_name.insert_one(item)
        await ctx.send(f'Added {guild.name} to the system, you can now use the bot properly')
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Setup is ready')

async def setup(bot):
    await bot.add_cog(Setup(bot))