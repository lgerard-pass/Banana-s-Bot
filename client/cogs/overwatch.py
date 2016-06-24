from discord.ext import commands
from client.constants import *
import datetime
from client.errors import WrongChannelError
from client.util.util import parseDate

class Overwatch:
    """Commands related to Overwatch"""
    def __init__(self, bot):
        self.bot = bot


    def ow_channel_check(ctx):
        if (ctx.message.channel.id != overwatchChannelId):
            return False
        else:
            return True

    @commands.command(pass_context=True,no_pm=True)
    @commands.check(ow_channel_check)
    async def register(self,ctx, date: str):
        """Register for GO4 - Format : DD-MM. """
        try:
            my_date = parseDate(date)
            member = ctx.message.author
            if my_date < datetime.date.today() or (my_date.weekday() != 2 and my_date.weekday() != 6):
                raise ValueError()
            f = open('GO4_' + str(my_date) + '.reg', 'a+')
            f.seek(0, 0)
            content = f.read()
            if member.name in content:
                await self.bot.reply('Tu t\'es deja inscrit champion !')
            else:
                f.seek(0, 2)
                f.write(member.name + ' ' + str(datetime.datetime.now()) + '\n')
                await self.client.reply('Inscription prise en compte')
            f.close()
        except ValueError:
            await self.client.reply('Erreur dans la date donnée')

    @commands.command(pass_context=True,no_pm=True)
    @commands.check(ow_channel_check)
    async def unregister(self,ctx, date: str):
        """Unregister for GO4 - Format : DD-MM. """
        try:
            my_date = parseDate(date)
            member = ctx.message.author
            if my_date < datetime.date.today() or (my_date.weekday() != 2 and my_date.weekday() != 6):
                raise ValueError()
            f = open('GO4_' + str(my_date) + '.reg', 'r')
            f.seek(0, 0)
            lines = f.readlines()
            found = False
            for line in lines:
                if (line.startswith(member.name)):
                    lines.remove(line)
                    found = True
            f.close()
            if not found:
                raise LookupError()
            f = open('GO4_' + str(my_date) + '.reg', 'w')
            f.seek(0, 0)
            for line in lines:
                f.write(line)
            f.close()
            await self.bot.reply('Desinscription prise en compte')
        except ValueError:
            await self.bot.reply('Erreur dans la date donnee')
        except LookupError:
            await self.bot.reply('Tu n\'etais pas inscrit a cette date')

    @commands.command(pass_context=True,no_pm=True)
    @commands.check(ow_channel_check)
    async def whoplays(self,ctx, date: str):
        """Says who registered for GO4 - Format : DD-MM."""
        try:
            my_date = parseDate(date)
            if my_date < datetime.date.today() or (my_date.weekday() != 2 and my_date.weekday() != 6):
                raise ValueError()
            f = open('GO4_' + str(my_date) + '.reg', 'r')
            content = f.read()
            if content == '':
                raise FileNotFoundError()
            await self.bot.reply(content)
            f.close()
        except ValueError:
            await self.bot.reply('Erreur dans la date donnee')
        except FileNotFoundError:
            await self.bot.reply('Personne n\'est encore inscrit a cette date')

def setup(bot):
    n = Overwatch(bot)
    bot.add_cog(n)

