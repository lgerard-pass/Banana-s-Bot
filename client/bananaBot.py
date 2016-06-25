from discord.ext import commands
from .constants import *
import datetime
from client.cogs.overwatch import setup as setup_ow
from client.cogs.miscellaneous import setup as setup_misc
import discord
import asyncio
from client.games.hangman import *

class bananaBot():
    #Constructor
    def __init__(self,token):
        self.client = commands.Bot(command_prefix=commands.when_mentioned_or('!'),description=clientDesc)
        self.token = token

        #Defining bot inner variables
        self.game_running = False

        #------------------------Defining cogs---------------------------------------------------------
        setup_ow(self.client)
        setup_misc(self.client)

        # -----------------------Defining bot commands-------------------------------------------------
        @self.client.command(pass_context=True)
        async def hangman(ctx):
            """Launch a hangman game."""
            if ctx.message.channel.id == game_channel_id:
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
            else:
                if not(ctx.message.server is None):
                    await self.client.say("Wrong chat, go to : " + ctx.message.server.get_channel(game_channel_id).mention)



    # -----------------------Defining background tasks-------------------------------------------------


    def run(self):
        return self.client.run(self.token)