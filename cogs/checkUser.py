from discord.ext import commands
from dotenv import load_dotenv
import discord
from pymongo_get_database import get_database
from discord.ext.commands import MemberConverter
import os

load_dotenv()
guild_id = int(os.getenv("GUILD_ID"))


class CheckUser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="checkuser",
        with_app_command=True,
        description="Check if a user has been warned, banned, kicked, or muted",
    )
    @commands.has_permissions(administrator=True)
    async def checkUser(self, ctx, member: MemberConverter()):
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
        if not collection.find_one({"user_id": memberId, "guild": guild.id}):
            ctx.reply("This user has not been bad yet!")
        warns = collection.find_one({"user_id": memberId, "guild": guild.id})["warns"]
        # check if the member has been/is banned from the server
        banned = collection.find_one({"user_id": memberId, "guild": guild.id})["banned"]
        # check if the member has been/is kicked from the server
        kicked = collection.find_one({"user_id": memberId, "guild": guild.id})["kicked"]
        # check if the member has been/is muted in the server
        muted = collection.find_one({"user_id": memberId, "guild": guild.id})["muted"]

        # create embed
        embed = discord.Embed(
            title="User Check",
            description=f"Checking user {memberMention}",
            color=0x00FF00,
        )
        embed.add_field(name="Warns", value=warns, inline=False)
        embed.add_field(name="Banned", value=banned, inline=False)
        embed.add_field(name="Kicked", value=kicked, inline=False)
        embed.add_field(name="Muted", value=muted, inline=False)
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        embed.set_author(
            name="Poeks",
            icon_url="https://cdn.discordapp.com/app-icons/868469587426045973/e42d5623fc11af69f6a84dbef205f3ef.png?size=256",
        )
        # add link to discord bot server
        embed.add_field(
            name="Support",
            value="[Discord Server](https://discord.gg/3m8T6JX)",
            inline=False,
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(CheckUser(bot))
