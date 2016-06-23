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

client.counter = 0
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    client.counter = client.counter + 1
    if client.annoy and client.counter > 5:
        await client.send_message(message.channel,'Hum')
        client.counter = 0
    await client.process_commands(message)
#-----------------------Defining bot commands-------------------------------------------------
@client.command()
async def roll(dice : str):
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

@client.command(pass_context=True)
async def register(ctx,date : str):
    """Format : DD-MM. Register for GO4 at given date"""
    try:
        member = ctx.message.author
        day, month = map(int, date.split('-'))
        my_date = datetime.date(datetime.datetime.now().year, month, day)
        if my_date < datetime.date.today() or (my_date.weekday() != 2 and my_date.weekday() != 6):
                raise ValueError()
        f = open('GO4_' + str(my_date) + '.reg'  , 'a+')
        position = f.seek(0,0)
        content = f.read()
        if member.name in content :
                await client.say('Tu t\'es deja inscrit champion !')
        else:
                position = f.seek(0, 2)
                f.write(member.name + ' ' + str(datetime.datetime.now()) + '\n')
                await client.say('Inscription prise en compte')
        f.close()
    except ValueError:
                await client.say('Erreur dans la date donnee') 

@client.command(pass_context=True)
async def unregister(ctx,date : str):
    """Format : DD-MM. Unregister for GO4 at given date"""
    try:
        member = ctx.message.author
        day, month = map(int, date.split('-'))
        my_date = datetime.date(datetime.datetime.now().year, month, day)
        if my_date < datetime.date.today() or (my_date.weekday() != 2 and my_date.weekday() != 6):
                raise ValueError()
        f = open('GO4_' + str(my_date) + '.reg'  , 'r')
        f.seek(0,0)
        lines = f.readlines()
        found = False
        for line in lines:
                if(line.startswith(member.name)):
                    lines.remove(line)
                    found = True
        f.close()
        if not found :
               raise LookupError()
        f = open('GO4_' + str(my_date) + '.reg'  , 'w')
        f.seek(0,0)
        for line in lines:
                f.write(line)
        f.close()
        await client.say('Desinscription prise en compte')
    except ValueError:
                await client.say('Erreur dans la date donnee')
    except LookupError:
                await client.say('Tu n\'etais pas inscrit a cette date')

@client.command(pass_context=True)
async def whoplays(ctx,date : str):
    """Format : DD-MM. Says who registered for GO4 at given date"""
    try:
        day, month = map(int, date.split('-'))
        my_date = datetime.date(datetime.datetime.now().year, month, day)
        if my_date < datetime.date.today() or (my_date.weekday() != 2 and my_date.weekday() != 6):
              raise ValueError()
        f = open('GO4_' + str(my_date) + '.reg'  , 'r')
        content = f.read()
        if content == '':
             raise FileNotFoundError()
        await client.say(content)
        f.close()
    except ValueError:
              await client.say('Erreur dans la date donnee')
    except FileNotFoundError:
              await client.say('Personne n\'est encore inscrit a cette date')

client.annoy = False
@client.command(pass_context=True)
async def annoy(ctx):
    """Surprise"""
    if ctx.message.author.id  == '101590011652096000':
        client.annoy = not client.annoy
    else:
        await client.say('Toi t\'as pas le droit !')
#-----------------------Defining background tasks-------------------------------------------------
#This task will run in background and will remind everyone to go training 1hour beforehand
async def check_training():
    await client.wait_until_ready()
    channel = discord.Object(id=overwatchChannelId) #SENDS TO CHANNEL OVERWATCH IN BANANA'S DISCORD
    while not client.is_closed:
        now = datetime.datetime.now()
        if now.weekday()==0 or now.weekday()==3:
            if now.hour==20:
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
client.loop.create_task(check_training())

#-----------------------Connectiong client-------------------------------------------------
client.run('MTk1NTEzNjMyMzI1NTAwOTI4.Ck1pGg.QXy7_6epx1q3ex-qSv3oXwjB0CQ')
