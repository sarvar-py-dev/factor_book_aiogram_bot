import os

from dotenv import load_dotenv
from redis_dict import RedisDict

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_LIST = [int(os.getenv("ADMIN")), ]
# host=os.getenv('REDIS_HOST'), port=os.getenv("REDIS_PORT")
database = RedisDict('books')
# , host=os.getenv('REDIS_HOST'), port=os.getenv("REDIS_PORT")