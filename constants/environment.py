import os
from dotenv import load_dotenv

ENVIRONMENT = os.getenv('ENVIRONMENT')
if ENVIRONMENT == None or ENVIRONMENT != 'production':
    load_dotenv()

DISCORD_TOKEN = str(os.getenv('DISCORD_TOKEN'))
DATABASE_URL = str(os.getenv('DATABASE_URL'))
