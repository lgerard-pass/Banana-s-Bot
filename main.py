from client.bananaBot import bananaBot
import discord 
import logging 

logger = logging.getLogger('discord') 
logger.setLevel(logging.DEBUG) 
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w') 
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#Read token from file
f = open('token', 'r')
token = f.read().strip()

#Launch bot 
bot = bananaBot(token)
bot.runMainLoop()
