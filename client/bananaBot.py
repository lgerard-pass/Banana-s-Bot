from discord.ext import commands
from .constants import *
from client.cogs.overwatch import setup as setup_ow
from client.cogs.miscellaneous import setup as setup_misc
from client.cogs.game import setup as setup_game
from client.cogs.music import setup as setup_music


class bananaBot():
    #Constructor
    def __init__(self,token):
        self.client = commands.Bot(command_prefix=commands.when_mentioned_or('!'),description=clientDesc)
        self.token = token
        #------------------------Setting up cogs---------------------------------------------------------
        setup_ow(self.client)
        setup_misc(self.client)
        setup_game(self.client)
        setup_music(self.client)

    def run(self):
        return self.client.run(self.token)