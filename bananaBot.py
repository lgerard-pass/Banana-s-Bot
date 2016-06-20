import discord
import asyncio
from discord.ext import commands
import datetime
import random


#Creating client
description = "Bot for Banana's discord"
client = commands.Bot(command_prefix='!', description=description)

bananasDiscordId = '101591369981632512'
overwatchChannelId = '173417024825982976'

#-----------------------Defining events-------------------------------------------------
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    newgame = discord.Game(name="with your mom")
    await client.change_status(game=newgame, idle=False)

#-----------------------Defining bot commands-------------------------------------------------
@client.command()
async def roll(dice : str):
    threshold = 200
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await client.say('Format has to be in NdN!')
        return
    if rolls > 200 or rolls < 1 or limit > 500 or limit < 2 :
        await client.say('T\'as que ca a branler de faire des jets pourraves ?')
    else:
        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await client.say(result)


#-----------------------Defining background tasks-------------------------------------------------
#This task will run in background and will remind everyone to go training 1hour beforehand
async def check_training():
    await client.wait_until_ready()
    channel = discord.Object(id=overwatchChannelId) #SENDS TO CHANNEL OVERWATCH IN BANANA'S DISCORD
    while not client.is_closed:
        now = datetime.datetime.now()
        if now.weekday()==0 or now.weekday()==3:
            if now.hour==19:
                role = discord.utils.find(lambda r: r.name == 'overwatch_players', client.get_server(bananasDiscordId).roles) 
                message = role.mention + ' Yo mes ptits poulets, oubliez pas le training de ce soir de 21h a 23h, sinon Loulou il va raler !'
                await client.send_message(channel, message)
        elif now.weekday()==5:
            if now.hour==15:
                role = discord.utils.find(lambda r: r.name == 'overwatch_players', client.get_server(bananasDiscordId).roles)
                message = role.mention + ' Yo mes ptits poulets, oubliez pas le training de cette apres-midi de 16h a 18h, sinon Loulou il va raler !'
                await client.send_message(channel, message)
        await asyncio.sleep(3600) # task runs every hour

#-----------------------Launching background task-------------------------------------------------
#client.loop.create_task(check_training())

#-----------------------Connectiong client-------------------------------------------------
client.run('MTkzNDk3MzA1MDEyMjQwMzg1.CkYP6A.dx6V_0bgCAsaa5GkRDr8ZEA6beg')
