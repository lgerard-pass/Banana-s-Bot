from os import listdir
from discord.ext import commands
from client.constants import *
import datetime
from client.util.util import parseDate
import discord
import asyncio
from ctypes.util import find_library
from collections import deque
import os.path
class Music:
    """Commands related to music playback"""
    def __init__(self, bot):
        self.bot = bot
        self.voice = None
        self.player = None
        self.playlist = deque(maxlen=3)
        discord.opus.load_opus(find_library("opus"))

    def playNextSong(self):
        if not (self.voice == None):
            if not (self.player == None):
                self.player.stop()
                self.player = None
                if(len(self.playlist) > 0):
                    self.player = self.playlist.popleft()
                    self.player.start()

    @commands.command(pass_context=True,no_pm=True)
    async def kaamelott(self,ctx,line : str):
        """Plays a given kaamelott sound"""
        await self.bot.delete_message(ctx.message)
        filename = '/media/USBHDD/sounds/' + line + '.mp3'
        if os.path.isfile(filename):
            if not(self.voice == None):
                self.player = self.voice.create_ffmpeg_player(filename)
                self.player.start()
            else:
                await self.bot.reply("Connecte moi à un channel d\'abord")
        else:
            await self.bot.reply("Le son n'existe pas")
    
    @commands.command(pass_context=True,no_pm=True,enabled=True)
    async def listkaamelott(self,ctx):
        """List all kamelott sounds"""
        await self.bot.delete_message(ctx.message)
        string = ''
        for filename in listdir('/media/USBHDD/sounds'):
            if len(filename) + len(string) >= 1500:
                await self.bot.reply(string)
                string = ''
            string = string + filename + '\n'
        await self.bot.reply(string)

    @commands.command(pass_context=True, no_pm=True,enabled=True)
    async def jointheparty(self, ctx, channelName : str):
        """Joins the voice channel given in argument"""
        channel = discord.utils.find(lambda m: m.name == channelName, ctx.message.server.channels)
        if not(channel == None):
            if not(self.voice == None):
                await self.voice.move_to(channel)
            self.voice = await self.bot.join_voice_channel(channel)
                 
    @commands.command(pass_context=True,no_pm=True,enabled=False)
    async def play(self,ctx,link : str):
        """Plays the audio of a youtube link"""
        await self.bot.delete_message(ctx.message)
        if self.player is None :
            if not(self.voice == None):
                self.player = await self.voice.create_ytdl_player(link,after=self.playNextSong)
                self.player.start()
            else:
                await self.bot.reply("Connecte moi à un channel d\'abord")
        else:
            await self.bot.reply("Il faut arreter la chanson avant d\'en lancer une autre")

    @commands.command(pass_context=True,no_pm=True,enabled=False)
    async def addToList(self, ctx, link: str):
        """Adds a song to the playlist
           No more than 3 songs can be put in the gueue before it starts removing other songs
        """
        await self.bot.delete_message(ctx.message)
        self.playlist.append(await self.voice.create_ytdl_player(link,after=self.playNextSong))
        await self.bot.reply("Chanson bien ajoutée, poulet !")

    @commands.command(pass_context=True,no_pm=True,enabled=False)
    async def stop(self,ctx):
        """Stops the current song and removes current playlist"""
        await self.bot.delete_message(ctx.message)
        self.playlist = deque(maxlen=3)
        if not(self.player == None):
            self.player.stop()
        self.player = None
        await self.bot.reply("Playlist et lecture en cours vidées")
    
    @commands.command(pass_context=True,no_pm=True,enabled=False)
    async def pause(self,ctx):
        """Pauses the current song"""
        if not(self.player == None):
            self.player.pause()
            await self.bot.delete_message(ctx.message)
            await self.bot.reply("Chanson mise en pause")

    @commands.command(pass_context=True,no_pm=True,enabled=False)
    async def resume(self):
        """Resumes the current song"""
        if not(self.player == None):
            self.player.resume()
            await self.bot.delete_message(ctx.message)
            await self.bot.reply("Chanson relancée")

    @commands.command(no_pm=True)
    async def leavetheparty(self):
        """Disconnects the bot from voice chat"""
        if not(self.voice == None):
            await self.voice.disconnect()


def setup(bot):
    n = Music(bot)
    bot.add_cog(n)

