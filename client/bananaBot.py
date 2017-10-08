from discord.ext import commands
from .constants import *
import time
import asyncio
from discord import ConnectionClosed
#from client.cogs.overwatch import setup as setup_ow
from client.cogs.miscellaneous import setup as setup_misc
from client.cogs.game import setup as setup_game
from client.cogs.music import setup as setup_music
from client.cogs.twitch import setup as setup_twitch

class bananaBot():
    #Constructor
    def __init__(self,token):
        self.client = commands.Bot(command_prefix=commands.when_mentioned_or('!'),description=clientDesc)
        self.token = token
        #------------------------Setting up cogs---------------------------------------------------------
        #setup_ow(self.client)
        setup_misc(self.client)
        #setup_game(self.client)
        setup_music(self.client)
        #setup_twitch(self.client)

    def runMainLoop(self):
        while(True):
            loop = asyncio.get_event_loop()
            try:
                loop.run_until_complete(self.client.login(self.token))
                loop.run_until_complete(self.client.connect())
            except KeyboardInterrupt:
                loop.run_until_complete(self.client.logout())
                print('test')
            finally:
                loop.close()
