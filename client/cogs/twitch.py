from discord.ext import commands
import discord
import asyncio
import http.client
from client.constants import *
import json

class Twitch:
    def __init__(self,bot):
        self.bot=bot
        self.runningStreams = []
    
    async def check_ow_stream(self):
        await self.bot.wait_until_ready()
        channel = discord.Object(id=overwatchChannelId)  # SENDS TO CHANNEL OVERWATCH IN BANANA'S DISCORD
        while not self.bot.is_closed:
            conn = http.client.HTTPSConnection("api.twitch.tv")
            headers = {
                'accept':"application/vnd.twitchtv.v3+json"
            }
            conn.request("GET","/kraken/streams/?channel=esl_alphacast%2CESL_Overwatch%2Csgdq%2Cogtv%2Cogamingsc2",headers=headers)
            res = conn.getresponse()
            data = res.read()
            data = data.decode("utf-8")
            parsedData = json.loads(data)
            stillRunning = []
            for element in parsedData["streams"]:
                if element["channel"]["name"] in self.runningStreams:
                    stillRunning += [element["channel"]["name"]]
                else:
                    str = element["channel"]["name"] + ' est en live : ' + element["channel"]["url"] + '\n' + element["preview"]["medium"] 
                    stillRunning += [element["channel"]["name"]]
                    await self.bot.send_message(channel,str)
            self.runningStreams = stillRunning
            await asyncio.sleep(120)

def setup(bot):
    n = Twitch(bot)
    bot.loop.create_task(n.check_ow_stream())
    return n
