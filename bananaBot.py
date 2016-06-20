import discord
import asyncio
import datetime
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    newgame = discord.Game(name="with your mom")
    await client.change_status(game=newgame, idle=False)

async def check_training():
    await client.wait_until_ready()
    channel = discord.Object(id='173417024825982976')
    while not client.is_closed:
        now = datetime.datetime.now()
        if now.weekday()==0 or now.weekday()==3:
            if now.hour==17:
                message='@overwatch_players Yo mes ptits poulets, oubliez pas le training de ce soir'
                await client.send_message(channel, message)
        elif now.weekday()==5:
            pass
        await asyncio.sleep(3600) # task runs every 60 seconds

client.loop.create_task(check_training())
client.run('MTkzNDk3MzA1MDEyMjQwMzg1.CkYP6A.dx6V_0bgCAsaa5GkRDr8ZEA6beg')
