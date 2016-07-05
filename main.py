from client.bananaBot import bananaBot
from client.constants import *
import discord 
import logging 

logger = logging.getLogger('discord') 
logger.setLevel(logging.DEBUG) 
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w') 
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#bot = bananaBot(token_test)
bot = bananaBot(token)
bot.run()
