import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_HOST = os.getenv('MONGODB_HOST') or 'localhost'
MONGODB_PORT = int(os.getenv('MONGODB_PORT') or '27017')
WEEKSET = os.getenv('WEEKSET')
WEEKDB = os.getenv('WEEKDB')

async def db_setup():
    client = AsyncIOMotorClient(MONGODB_HOST, MONGODB_PORT)
    all_week = client[WEEKSET]
    weekdaydb = all_week[WEEKDB]
    return weekdaydb
