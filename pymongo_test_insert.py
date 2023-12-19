from pymongo_get_database import get_database
from dateutil import parser

expiry = parser.parse("2021-08-01T00:00:00.000Z")

item_1 = {
    "name": "item_1",
    "guild_id": 123456789,
    "expiry_date": expiry
}

# get database
dbname = get_database()
collection_name = dbname["guild"]

collection_name.insert_one(item_1)