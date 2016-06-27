from discord.ext import commands
from client.constants import adminId
import random
import discord

class Miscellaneous:
    """Miscellaneous commands"""
    def __init__(self, bot):
        self.bot = bot
        self.annoyToggle = False
        self.msg_counter = 0

    @commands.command()
    async def roll(self,dice: str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await self.bot.reply('Format has to be in NdN!')
            return
        if rolls > 200 or rolls < 1 or limit > 500 or limit < 2:
            await self.bot.reply('T\'as que ca a branler de faire des jets pourraves ?')
        else:
            result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
            await self.bot.reply(result)


    @commands.command(pass_context=True,hidden=True)
    async def annoy(self,ctx):
        """Send an annoying message every 5 messages received"""
        if ctx.message.author.id == adminId:
            self.annoyToggle = not self.annoyToggle
        else:
            await self.bot.reply('Toi t\'as pas le droit !')

    @commands.command(pass_context=True, hidden=True,no_pm=True)
    async def oracle(self, ctx, question:str):
        """Answers a very important question"""
        if ctx.message.author != self.bot.user:
            n = len(ctx.message.content) % 7
            if(n == 0):
                str = 'J\'ai besoin de temps pour me concentrer !'
            elif(n == 1):
                str = 'Oui'
            elif(n == 2):
                str = 'Non'
            elif(n == 3):
                str = 'Je ne peux pas répondre à cette question'
            elif(n == 4):
                str = 'Oui mais honnêtement je suis pas sur, au pire lance un dé'
            elif(n == 5):
                str = 'Concrètement c\'est mort'
            elif(n == 6):
                str = 'A mon avis non'
            elif(n == 7):
                str = 'Non, sinon attention au claquage'
            if 'travail' in question:
                if ctx.message.author.name == 'Garma':
                    str = 'Comme si ma réponse allait changer quelquechose'
                else:
                    str = 'Non c\'est pas une bonne idée'
            elif 'aujourd\'hui' in question:
                str = 'Non non pas aujourd\'hui'
            await self.bot.reply(str)


    async def on_message(self,message):
        if message.author == self.bot.user:
            return
        self.msg_counter += 1
        if self.annoyToggle and self.msg_counter > 5:
            await self.bot.send_message(message.channel, 'Hum')
            self.msg_counter = 0

    async def on_ready(self):
        print('Logged in as')
        print(self.bot.user.name)
        print(self.bot.user.id)
        print('------')
        newgame = discord.Game(name="with your mom")
        await self.bot.change_status(game=newgame, idle=False)


def setup(bot):
    n = Miscellaneous(bot)
    bot.add_cog(n)
