from discord.ext import commands
from pymongo_get_database import get_database

class SetPrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setprefix(self, ctx, arg1=None):
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
        if not guild_data:
            await ctx.send(f"{guild.name} is not in the setted up yet! Use the command `!setup` to add the guild to the system")
            return
        
        # check if arg1 is valid
        if len(arg1) > 1:
            await ctx.send('The prefix can only be one character long')
            return
        
        # get prefix
        prefix = guild_data["prefix"]
        
        if arg1 == None:
            await ctx.send(f'The current prefix is `{prefix}`')
            return
        else:
            # update prefix
            collection_name.update_one({"guild_id": guild.id}, {"$set": {"prefix": arg1}})
            await ctx.send(f'Prefix changed to `{arg1}`')
            return
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Setup is ready')

async def setup(bot):
    await bot.add_cog(SetPrefix(bot))