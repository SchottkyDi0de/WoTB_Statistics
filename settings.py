import os
from dotenv import load_dotenv

load_dotenv()

WG_APP_ID = os.getenv('WG_APP_ID')
bot_settings = {
'TOKEN':os.getenv('DISCORD_TOKEN'),
'name':'[HVOLT] WoTB Statistics',
'command_prefix':'!'
}