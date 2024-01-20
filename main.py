# imports
import discord
import os
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from pymongo_get_database import get_database

# load environment variables
load_dotenv()
token = os.getenv("DISCORD_TOKEN")


async def get_prefix(bot, message):
    # get database
    dbname = get_database()
    collection_name = dbname["guild"]

    # get prefix
    guild_id = message.guild.id
    guild = collection_name.find_one({"guild_id": guild_id})
    prefix = guild["prefix"] if guild else "!"
    return prefix


# create bot
class Bot(commands.Bot):
    def __init__(
        self,
    ):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=get_prefix, intents=intents)

    async def on_command_error(self, ctx, error) -> None:
        await ctx.reply(error, ephemeral=True)

    # create bot and get the command prefix from the database


bot = Bot()

bot.remove_command("help")


# load cogs
@bot.event
async def on_ready():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            command = filename[:-3]
            await bot.load_extension(f"cogs.{command}")
            print(f"{command} loaded")
    print("Bot is ready")


# on added to guild add to mongo database
@bot.event
async def on_guild_join(guild):
    # get database
    dbname = get_database()
    collection_name = dbname["guild"]

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
    print(f"Added {guild.name} to database")


# on removed from guild remove from mongo database
@bot.event
async def on_guild_remove(guild):
    # get database
    dbname = get_database()
    collection_name = dbname["guild"]

    # remove item
    collection_name.delete_one({"guild_id": guild.id})
    print(f"Removed {guild.name} from leveling database")


# when a member joins the server add them to the leveling database
@bot.event
async def on_member_join(member):
    # get database
    dbname = get_database()
    collection_name = dbname["leveling"]

    # check if leveling is enabled
    guild_id = member.guild.id
    guild = dbname["guild"].find_one({"guild_id": guild_id})
    leveling = guild["leveling"] if guild else False
    if not leveling:
        return

    # create item
    item = {
        "name": member.name,
        "guild_id": member.guild.id,
        "user_id": member.id,
        "level": 1,
        "xp": 0,
        "xp_to_level": 100,
        "expiry_date": None,
    }

    # insert item
    collection_name.insert_one(item)
    print(f"Added {member.name} to leveling database")


# when a member leaves the server remove them from the leveling database
@bot.event
async def on_member_remove(member):
    # get database
    dbname = get_database()
    collection_name = dbname["leveling"]

    # remove item
    collection_name.delete_one({"user_id": member.id})
    print(f"Removed {member.name} from leveling database")


# when a message is sent add xp to the user
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    # check if leveling is enabled
    dbname = get_database()
    guild_id = message.guild.id

    guild = dbname["guild"].find_one({"guild_id": guild_id})
    leveling = guild["leveling"] if guild else False

    if leveling:
        # if the message is from a bot do nothing

        # get database
        collection_name = dbname["leveling"]

        # get user with the correct guild id and user id
        user = collection_name.find_one(
            {"guild_id": message.guild.id, "user_id": message.author.id}
        )
        # if user is not in the database add them
        if not user:
            # create item
            item = {
                "name": message.author.name,
                "guild_id": message.guild.id,
                "user_id": message.author.id,
                "level": 1,
                "xp": 0,
                "xp_to_level": 100,
                "expiry_date": None,
            }

            # insert item
            collection_name.insert_one(item)
            print(f"Added {message.author.name} to leveling database")

        # add xp to user
        else:
            # get xp and xp_to_level
            xp = user["xp"]
            xp_to_level = user["xp_to_level"]
            # add xp
            xp += 50
            # if xp is equal to xp_to_level level up
            if xp >= xp_to_level:
                # get level
                level = user["level"]
                # level up
                level += 1
                # get new xp_to_level
                xp_to_level = (level * 10) ** 2
                # update database
                collection_name.update_one(
                    {"guild_id": message.guild.id, "user_id": message.author.id},
                    {"$set": {"level": level, "xp": xp, "xp_to_level": xp_to_level}},
                )
                print(f"{message.author.name} leveled up to level {level}")
                # send message
                await message.channel.send(
                    f"{message.author.mention} leveled up to level {level}"
                )
            # if xp is not equal to xp_to_level update database
            else:
                collection_name.update_one(
                    {"guild_id": message.guild.id, "user_id": message.author.id},
                    {"$set": {"xp": xp}},
                )

    await bot.process_commands(message)


# run bot
bot.run(token)
