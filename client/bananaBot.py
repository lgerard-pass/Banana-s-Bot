from discord.ext import commands
from .constants import *
import datetime
import random
import discord
import asyncio
from client.games.hangman import *

class bananaBot():
    #Constructor
    def __init__(self,token):
        self.client = commands.Bot(command_prefix='!', description=clientDesc)
        self.token = token

        #Defining bot inner variables
        self.client.annoy = False
        self.client.msg_counter = 0
        self.game_running = False

        # -----------------------Defining events-------------------------------------------------
        @self.client.event
        async def on_ready():
            print('Logged in as')
            print(self.client.user.name)
            print(self.client.user.id)
            print('------')
            newgame = discord.Game(name="with your mom")
            await self.client.change_status(game=newgame, idle=False)

        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return
            self.client.msg_counter = self.client.msg_counter + 1
            if self.client.annoy and self.client.msg_counter > 5:
                await self.client.send_message(message.channel, 'Hum')
                self.client.msg_counter = 0
            await self.client.process_commands(message)
        
        # -----------------------Defining bot commands-------------------------------------------------
        @self.client.command()
        async def roll(dice: str):
            """Rolls a dice in NdN format."""
            try:
                rolls, limit = map(int, dice.split('d'))
            except Exception:
                await self.client.say('Format has to be in NdN!')
                return
            if rolls > 200 or rolls < 1 or limit > 500 or limit < 2:
                await self.client.say('T\'as que ca a branler de faire des jets pourraves ?')
            else:
                result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
                await self.client.say(result)

        @self.client.command()
        async def hangman():
            """Launch a hangman game."""
            if self.game_running:
                await self.client.say("Une partie est déjà en cours, attendez la fin !")
                return
            self.game_running = True
            remaining_tries = nb_tries
            found_letters = []
            word = selectWord().upper()
            print(word)
            revealedWord = get_revealed_word(word,found_letters)
            print(revealedWord)
            await self.client.say('Allez c\'est tipar')
            won = False
            lost = False
            while not(won) and not(lost):
                await self.client.say("```" + revealedWord + '\n' + "Tentatives restantes : "  + str(remaining_tries) + "```")
                answer = await self.client.wait_for_message(timeout=10.0, check=hang_check)
                if answer is None :
                    await self.client.say("Vous avez été trop long(s), il faut répondre sous 10 secondes\nFin de la partie")
                    self.game_running = False
                    return
                else:
                    answer = answer.content.upper()
                    if answer in found_letters:
                        await self.client.say("Vous avez déjà choisi cette lettre.")
                    elif answer in word:
                        found_letters.append(answer)
                    else:
                        remaining_tries -= 1
                    revealedWord = get_revealed_word(word,found_letters)
                won,lost = evaluate_game(word,revealedWord,remaining_tries)
            if won :
                await self.client.say("```Bien joué ! Le mot était : " + word + "```")
            else :
                await self.client.say("```Vous êtes mauvais ! Le mot était : " + word + "```")
            self.game_running = False

        @self.client.command(pass_context=True)
        async def register(ctx, date: str):
            """Format : DD-MM. Register for GO4 at given date"""
            if (ctx.message.channel.id == overwatchChannelId):
                try:
                    member = ctx.message.author
                    day, month = map(int, date.split('-'))
                    my_date = datetime.date(datetime.datetime.now().year, month, day)
                    if my_date < datetime.date.today() or (my_date.weekday() != 2 and my_date.weekday() != 6):
                        raise ValueError()
                    f = open('GO4_' + str(my_date) + '.reg', 'a+')
                    position = f.seek(0, 0)
                    content = f.read()
                    if member.name in content:
                        await self.client.say('Tu t\'es deja inscrit champion !')
                    else:
                        position = f.seek(0, 2)
                        f.write(member.name + ' ' + str(datetime.datetime.now()) + '\n')
                        await self.client.say('Inscription prise en compte')
                    f.close()
                except ValueError:
                    await self.client.say('Erreur dans la date donnee')
    
        @self.client.command(pass_context=True)
        async def unregister(ctx, date: str):
            """Format : DD-MM. Unregister for GO4 at given date"""
            if(ctx.message.channel.id == overwatchChannelId):
                try:
                    member = ctx.message.author
                    day, month = map(int, date.split('-'))
                    my_date = datetime.date(datetime.datetime.now().year, month, day)
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
                    await self.client.say('Desinscription prise en compte')
                except ValueError:
                    await self.client.say('Erreur dans la date donnee')
                except LookupError:
                    await self.client.say('Tu n\'etais pas inscrit a cette date')
    
        @self.client.command(pass_context=True)
        async def whoplays(ctx, date: str):
            """Format : DD-MM. Says who registered for GO4 at given date"""
            if (ctx.message.channel.id == overwatchChannelId):
                try:
                    day, month = map(int, date.split('-'))
                    my_date = datetime.date(datetime.datetime.now().year, month, day)
                    if my_date < datetime.date.today() or (my_date.weekday() != 2 and my_date.weekday() != 6):
                        raise ValueError()
                    f = open('GO4_' + str(my_date) + '.reg', 'r')
                    content = f.read()
                    if content == '':
                        raise FileNotFoundError()
                    await self.client.say(content)
                    f.close()
                except ValueError:
                    await self.client.say('Erreur dans la date donnee')
                except FileNotFoundError:
                    await self.client.say('Personne n\'est encore inscrit a cette date')
    
        @self.client.command(pass_context=True)
        async def annoy(ctx):
            """Surprise"""
            if ctx.message.author.id == adminId:
                self.client.annoy = not self.client.annoy
            else:
                await self.client.say('Toi t\'as pas le droit !')

                # -----------------------Defining background tasks-------------------------------------------------

        # This task will run in background and will remind everyone to go training 1 hour beforehand
    async def check_training(self):
        await self.client.wait_until_ready()
        channel = discord.Object(id=overwatchChannelId)  # SENDS TO CHANNEL OVERWATCH IN BANANA'S DISCORD
        while not self.client.is_closed:
            now = datetime.datetime.now()
            if now.weekday() == 0 or now.weekday() == 3:
                if now.hour == 20:
                    role = discord.utils.find(lambda r: r.name == 'overwatch_players',
                                              self.client.get_server(bananasDiscordId).roles)
                    message = role.mention + ' Yo mes ptits poulets, oubliez pas le training de ce soir de 21h a 23h, sinon Loulou il va raler !'
                    await self.client.send_message(channel, message)
            elif now.weekday() == 5:
                if now.hour == 15:
                    role = discord.utils.find(lambda r: r.name == 'overwatch_players', self.client.get_server(bananasDiscordId).roles)
                    message = role.mention + ' Yo mes ptits poulets, oubliez pas le training de cette apres-midi de 16h a 18h, sinon Loulou il va raler !'
                    await self.client.send_message(channel, message)
            await asyncio.sleep(3600)  # task runs every hour

    def run(self):
        self.client.loop.create_task(self.check_training())
        return self.client.run(self.token)