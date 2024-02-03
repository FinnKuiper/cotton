import discord
from discord.ext import commands
from discord import app_commands
from pymongo_get_database import get_database
from dotenv import load_dotenv
import os

load_dotenv()
guild_id = int(os.getenv("GUILD_ID"))


class GuildSettings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="guildsettings",
        with_app_command=True,
        description="Get the guild info",
    )
    @app_commands.guilds(discord.Object(id=guild_id))
    @commands.has_permissions(administrator=True)
    async def guildsettings(self, ctx):
        # get database
        dbname = get_database()
        collection_name = dbname["guild"]

        # get guild info
        guild_data = collection_name.find_one({"guild_id": ctx.guild.id})
        if not guild_data:
            await ctx.send(
                f"{ctx.guild.name} is not in the setted up yet! Use the command `!setup` to add the guild to the system"
            )
            return

        # get guild info
        guild_name = guild_data["name"]
        guild_prefix = guild_data["prefix"]
        update_channel = guild_data["update_channel"]
        welcome_channel = guild_data["welcome_channel"]
        leveling = guild_data["leveling"]

        guild_users = ctx.guild.member_count

        # create embed with the guild info
        embed = discord.Embed(
            title=f"{guild_name} Info",
            color=0xEB34E5,
            timestamp=ctx.message.created_at,
        )
        embed.add_field(name="prefix", value=guild_prefix, inline=True)
        embed.add_field(name="users", value=guild_users, inline=True)
        embed.add_field(name="update channel", value=update_channel, inline=True)
        embed.add_field(name="welcome channel", value=welcome_channel, inline=True)
        embed.add_field(name="leveling", value=leveling, inline=True)
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Setup is ready")


async def setup(bot):
    await bot.add_cog(GuildSettings(bot))
