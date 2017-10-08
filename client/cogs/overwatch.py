from discord.ext import commands
from client.constants import *
from datetime import datetime
from client.util.util import parseDate
from datetime import timezone
from datetime import timedelta
import discord
import asyncio
import requests
import bs4
import re

class Match:
    team1 = ""
    team2 = ""
    date = None
    tournament = ""

    def __init__(self,team1,team2,date,tournament):
        self.team1 = team1
        self.team2 = team2
        self.date = date.replace(tzinfo=timezone.utc).astimezone(tz=None)
        self.tournament = tournament

    def __str__(self):
        return  self.team1 + ' vs. ' + self.team2 + " - " + self.date.strftime(
                '%d/%m at %H:%M') + " for " + self.tournament

class Overwatch:
    """Commands related to Overwatch"""
    notified_matches = []
    def __init__(self, bot):
        self.bot = bot


    def ow_channel_check(ctx):
        if (ctx.message.channel.id != overwatchChannelId):
            return False
        else:
            return True

    @commands.command(pass_context=True,no_pm=True,enable=False)
    @commands.check(ow_channel_check)
    async def register(self,ctx, date : str):
        """Register for GO4 - Format : DD-MM."""
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
                await self.bot.reply('Inscription prise en compte pour le ' + my_date.strftime("%d/%m"))
            f.close()
        except ValueError:
            await self.bot.reply('Erreur dans la date donnée')

    @commands.command(pass_context=True,no_pm=True,enabled=False)
    @commands.check(ow_channel_check)
    async def unregister(self,ctx, date: str):
        """Unregister for GO4 - Format : DD-MM."""
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
            await self.bot.reply('Desinscription prise en compte pour le ' + my_date.strftime("%d/%m"))
        except ValueError:
            await self.bot.reply('Erreur dans la date donnee')
        except LookupError:
            await self.bot.reply('Tu n\'etais pas inscrit a cette date (le ' + + my_date.strftime("%d/%m") + ')')

    @commands.command(pass_context=True,no_pm=True,enabled=False)
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
            answer = '\nRésumé des inscriptions pour le : ' + my_date.strftime("%d/%m") + '\n' + content
            await self.bot.reply(answer)
            f.close()
        except ValueError:
            await self.bot.reply('Erreur dans la date donnee')
        except FileNotFoundError:
            await self.bot.reply('Personne n\'est encore inscrit a cette date (le ' + my_date.strftime("%d/%m") + ')')

            # This task will run in background and will remind everyone to go training 1 hour beforehand

    @commands.command(no_pm=True)
    @commands.check(ow_channel_check)
    async def upcomingMatches(self):
        answer = '```'
        matches = getMatches()
        for match in matches:
            answer += str(match)
            answer += "\n"
        await self.bot.say(answer + "```")

    async def check_training(self):
        await self.bot.wait_until_ready()
        channel = discord.Object(id=overwatchChannelId)  # SENDS TO CHANNEL OVERWATCH IN BANANA'S DISCORD
        while not self.bot.is_closed:
            now = datetime.datetime.now()
            if now.weekday() == 0 or now.weekday() == 3:
                if now.hour == 20:
                    role = discord.utils.find(lambda r: r.name == 'overwatch_players',
                                              self.bot.get_server(bananasDiscordId).roles)
                    message = role.mention + ' Yo mes ptits poulets, oubliez pas le training de ce soir de 21h a 23h, sinon Loulou il va raler !'
                    await self.bot.send_message(channel, message)
            elif now.weekday() == 5:
                if now.hour == 15:
                    role = discord.utils.find(lambda r: r.name == 'overwatch_players',
                                              self.bot.get_server(bananasDiscordId).roles)
                    message = role.mention + ' Yo mes ptits poulets, oubliez pas le training de cette apres-midi de 16h a 18h, sinon Loulou il va raler !'
                    await self.bot.send_message(channel, message)
            await asyncio.sleep(3600)  # task runs every hour

    async def check_nextMatch(self):
        await self.bot.wait_until_ready()
        channel = discord.Object(id=overwatchChannelId)  # SENDS TO CHANNEL OVERWATCH IN BANANA'S DISCORD
        matches = getMatches()
        current_datetime = datetime.now().astimezone(tz=None)
        for match in matches:
            delta = match.date - current_datetime
            if(match not in self.notified_matches and match.date - current_datetime > timedelta() and match.date - current_datetime < timedelta(minutes=30)):
                message = "Match incoming : \n" + str(match)
                await self.bot.send_message(channel, message)
                self.notified_matches += [match]
        await asyncio.sleep(60)  # task runs every minute



def getMatches():
    response = requests.get(overwatchLiquipediaURL)
    soup = bs4.BeautifulSoup(response.text)
    matches = soup.findAll("table", {"class": "infobox_matches_content"})
    parsed_matches = []
    for match in matches:
        mystring = match.text.replace('\n\n', '').replace('\n', '/').replace(' Template:Abbr/UTC', ' UTC/')
        search = re.search(r'(.*) vs. (.*)\/(.*)\/(.*)\/', mystring)
        team1 = search.group(1)
        team2 = search.group(2)

        date = search.group(3)
        parsed_date = datetime.strptime(date, '%B %d, %Y - %H:%M %Z')

        tournament = search.group(4)
        entire_match = Match(team1,team2,parsed_date,tournament)
        parsed_matches += [entire_match]
    return parsed_matches



def setup(bot):
    n = Overwatch(bot)
    #bot.loop.create_task(n.check_training())
    bot.loop.create_task(n.check_nextMatch())
    bot.add_cog(n)

