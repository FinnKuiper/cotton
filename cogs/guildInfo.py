import discord
from discord.ext import commands
from pymongo_get_database import get_database

class GuildInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def guildinfo(self, ctx):
        # get database
        dbname = get_database()
        collection_name = dbname["guild"]

        # get guild info
        guild_data = collection_name.find_one({"guild_id": ctx.guild.id})
        if not guild_data:
            await ctx.send(f"{ctx.guild.name} is not in the setted up yet! Use the command `!setup` to add the guild to the system")
            return
        
        # get guild info
        guild_name = guild_data["name"]
        guild_prefix = guild_data["prefix"]
        guild_users = ctx.guild.member_count

        # create embed with the guild info
        embed = discord.Embed(title=f"{guild_name} Info", description=f"Prefix: {guild_prefix}\nUsers: {guild_users}", color=0x00ff00)
        await ctx.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Setup is ready')

async def setup(bot):
    await bot.add_cog(GuildInfo(bot))