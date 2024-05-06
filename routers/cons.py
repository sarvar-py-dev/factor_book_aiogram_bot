import os

from dotenv import load_dotenv
from redis_dict import RedisDict

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_LIST = [6126220359, ]

database = RedisDict('books')
