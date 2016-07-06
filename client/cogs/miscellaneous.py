from discord.ext import commands
from client.constants import adminId
from client.constants import private_channel_id_with_admin
import random
import discord

class Miscellaneous:
    """Miscellaneous commands"""
    def __init__(self, bot):
        self.bot = bot
        self.annoyToggle = False
        self.msg_counter = 0

    def check_pm(ctx):
        return ctx.message.channel.user.id == adminId

    @commands.command(hidden=True)
    @commands.check(check_pm)
    async def say(self,channelId:str,message:str):
        """Says something that has been given in private message"""
        print(channelId)
        print(message)
        await self.bot.send_message(self.bot.get_channel(channelId),message)

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

    @commands.command(pass_context=True,no_pm=True)
    async def highfive(self,ctx,user : discord.Member):
        """Gives someone a high five !"""
        await self.bot.say("Hey " + user.mention + " give me five ! o/")
        answer = await self.bot.wait_for_message(timeout=10.0, author=user, check=high_five_check)
        if answer is None :
            await self.bot.say("Hey " + user.mention + " ! FUCK YOU")
        else:
            await self.bot.say(user.mention + " Bien joué !")

    @commands.command(hidden=True)
    async def ping(self):
        """Pong."""
        await self.bot.say("Pong.")

    @commands.command(no_pm=True,pass_context=True)
    async def hug(self, ctx,target: str, intensity: int = 1, hidden: bool = False):
        """Hugs someone, because we're bunch of good ol' lads !

        Accepts three parameters:
        The user you want to hug as a string, not a mention
        The intensity of the hug as an integer defaults to 1
        Whether or not the message should be deleted as a boolean"""
        newTarget = discord.utils.get(ctx.message.server.members, name=target)
        if newTarget is None:
            newTarget = discord.utils.get(ctx.message.server.roles, name=target)
        if newTarget is None:
            await self.bot.say("Je ne peux pas caliner ce qui n\'existe pas")
            return
        name = " *" + newTarget.mention + "*"
        if intensity <= 0:
            msg = "(っ˘̩╭╮˘̩)っ" + name
        elif intensity <= 3:
            msg = "(っ´▽｀)っ" + name
        elif intensity <= 6:
            msg = "╰(*´︶`*)╯" + name
        elif intensity <= 9:
            msg = "(つ≧▽≦)つ" + name
        elif intensity >= 10:
            msg = "(づ￣ ³￣)づ" + name + " ⊂(´・ω・｀⊂)"
        await self.bot.say(msg)
        if hidden:
            await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True, no_pm=True)
    async def userinfo(self, ctx, user: discord.Member = None):
        """Shows users's informations

        Shows user info, user can be given in arguments as a mention, otherwise
        it will be the author of the command."""
        author = ctx.message.author
        if not user:
            user = author
        roles = [x.name for x in user.roles if x.name != "@everyone"]
        if not roles: roles = ["None"]
        data = "```python\n"
        data += "Name: {}\n".format(user.name)
        data += "ID: {}\n".format(user.id)
        passed = (ctx.message.timestamp - user.created_at).days
        data += "Created: {} ({} days ago)\n".format(user.created_at, passed)
        passed = (ctx.message.timestamp - user.joined_at).days
        data += "Joined: {} ({} days ago)\n".format(user.joined_at, passed)
        data += "Roles: {}\n".format(", ".join(roles))
        data += "Avatar: {}\n".format(user.avatar_url)
        data += "```"
        await self.bot.say(data)



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

def high_five_check(message):
    if (message.content == '\o'):
        return True 
    else:
        return False
