import discord
import asyncio
import http.client
from client.constants import *
import json
from urllib.parse import quote
from discord.ext import commands

class Twitch:
    def __init__(self,bot):
        self.bot=bot

    @commands.command(no_pm=True)
    async def getcois(self,category:str):
        """Retrieves watched channels of interest (COIs) from the list

        category : The category in which the channels should be retrieved. Can be either Overwatch,Other or Starcraft
        """
        if not (category in valid_streams_categories):
            await self.bot.reply("Mauvais catégorie donnée !")
            return
        f = open(category + 'COI', 'r')
        content = f.read()
        f.close()
        await self.bot.reply("La liste des channels surveillés pour la catégorie : " + category + "\n" + content)

    @commands.command(no_pm=True)
    async def deletecoi(self, channelName: str, category:str):
        """Removes a channel of interest (COI) from the list

        channelName : The name of the channel to remove
        category : The category in which the channel should be removed. Can be either Overwatch,Other or Starcraft
        """
        if not (category in valid_streams_categories):
            await self.bot.reply("Mauvais catégorie donnée !")
            return
        if (len(channelName) < 1 or len(channelName) > 50):
            await self.bot.reply("Nom de channel invalide !")
            return
        channelName = channelName.lower()
        f = open(category + 'COI', 'r')
        channels = f.read().split(',')
        f.close()
        try:
            channels.remove(channelName)
            f = open(category + 'COI', 'w')
            for i in range(0,len(channels)-1):
                f.write(channels[i] + ',')
            f.write(channels[len(channels)-1])
            f.close()
            await self.bot.reply("Channel bien retiré !")
        except:
            await self.bot.reply("Le channel n'existe pas")
            f.close()
            return
        return

    @commands.command(no_pm=True)
    async def addcoi(self,channelName:str,category:str):
        """Adds a channel of interest (COI) to the list

        channelName : The name of the channel to add
        category : The category in which the channel should be added. Can be either Overwatch,Other or Starcraft
        """
        if not(category in valid_streams_categories):
            await self.bot.reply("Mauvais catégorie donnée !")
            return
        if (len(channelName) < 1 or len(channelName) > 50):
            await self.bot.reply("Nom de channel invalide !")
            return
        channelName = channelName.lower()
        conn = http.client.HTTPSConnection("api.twitch.tv")
        headers = {
            'accept': "application/vnd.twitchtv.v3+json"
        }
        request = "/kraken/channels/" + quote(channelName)
        conn.request("GET", request, headers=headers)
        res = conn.getresponse()
        data = res.read()
        data = data.decode("utf-8")
        parsedData = json.loads(data)
        try:
            logo=parsedData["logo"]
            f = open(category + 'COI', 'a+')
            f.seek(0, 0)
            if channelName in f.read():
                await self.bot.reply("Channel déjà présent dans la liste")
                f.close()
                return
            f.seek(0, 2)
            f.write(',' + channelName)
            f.close()
            await self.bot.reply("Channel bien ajouté à la liste\n" + logo)
            return
        except KeyError:
            await self.bot.reply("Nom de channel valide, mais introuvable !")
            return

    async def check_streams(self,channel,filename):
        await self.bot.wait_until_ready()
        runningStreams = []
        while not self.bot.is_closed:
            conn = http.client.HTTPSConnection("api.twitch.tv")
            headers = {
                'accept':"application/vnd.twitchtv.v3+json"
            }
            f = open(filename, 'r')
            request = "/kraken/streams/?channel=" + quote(f.read().strip())
            f.close()
            conn.request("GET",request,headers=headers)
            res = conn.getresponse()
            data = res.read()
            data = data.decode("utf-8")
            parsedData = json.loads(data)
            stillRunning = []
            for element in parsedData["streams"]:
                if element["channel"]["name"] in runningStreams:
                    stillRunning += [element["channel"]["name"]]
                else:
                    str = element["channel"]["name"] + ' est en live : ' + element["channel"]["url"] + '\n' + element["preview"]["large"]
                    stillRunning += [element["channel"]["name"]]
                    await self.bot.send_message(channel,str)
            runningStreams = stillRunning
            await asyncio.sleep(600)

def setup(bot):
    n = Twitch(bot)
    bot.loop.create_task(n.check_streams(discord.Object(id=overwatchChannelId),'OverwatchCOI'))
    bot.loop.create_task(n.check_streams(discord.Object(id=sc2ChannelId),'StarcraftCOI'))
    bot.loop.create_task(n.check_streams(discord.Object(id=videogamesChannelId),'OtherCOI'))
    bot.add_cog(n)
