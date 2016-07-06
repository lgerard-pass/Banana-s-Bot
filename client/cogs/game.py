from discord.ext import commands
from client.constants import *
from client.games.hangman import *
from client.games.shifumi import *
import discord

class Game:
    def __init__(self, bot):
        self.bot = bot
        self.game_running = False

    def games_channel_check(ctx):
        if (ctx.message.channel.id != game_channel_id):
            return False
        else:
            return True

    @commands.command(pass_context=True,no_pm=True,hidden=True)
    @commands.check(games_channel_check)
    async def shifumi(self,ctx,p2 :discord.Member):
        """Launch a shifumi against someone"""
        if self.game_running:
            await self.bot.say("Une partie est déjà en cours, attendez la fin")
            return
        self.game_running = True
        chan = ctx.message.channel
        p1 = ctx.message.author
        await self.bot.say("Partie lancée entre " +  p1.mention + " et " + p2.mention)
        await self.bot.say(p1.mention + " fais ton choix !")
        a1 = await self.bot.wait_for_message(timeout=10.0,author=p1,channel=chan, check=shifumi_check)
        if a1 is None:
            await self.bot.say(p1.mention + "a été trop long, " + p2.mention + " gagne !")
            self.game_running = False
            return
        choice1 = a1.content
        await self.bot.delete_message(a1)
        await self.bot.say(p2.mention + " fais ton choix !")
        a2 = await self.bot.wait_for_message(timeout=10.0,author=p2,channel=chan, check=shifumi_check)
        if a2 is None:
            await self.bot.say(p2.mention + "a t trop long, " + p1.mention + " gagne ! ")
            self.game_running = False
            return
        choice2 = a2.content         
        await self.bot.delete_message(a2)
        sign = get_shifumi_winner(choice1,choice2)
        await self.bot.say(p1.mention + " "  + sign + " " + p2.mention)
        self.game_running = False

    @commands.command(pass_context=True,no_pm=True)
    @commands.check(games_channel_check)
    async def hangman(self,ctx):
        """Launch a hangman game.

        """
        if self.game_running:
            await self.bot.say("Une partie est déjà en cours, attendez la fin !")
            return
        self.game_running = True
        remaining_tries = nb_tries
        found_letters = []
        word = selectWord().upper()
        revealedWord = get_revealed_word(word, found_letters)
        await self.bot.say('Allez c\'est tipar')
        won = False
        lost = False
        while not (won) and not (lost):
            await self.bot.say("```" + revealedWord + '\n' + "Tentatives restantes : " + str(remaining_tries) + "```")
            answer = await self.bot.wait_for_message(timeout=10.0, check=hang_check)
            if answer is None:
                await self.bot.say(
                    "Vous avez été trop long(s), il faut répondre sous 10 secondes\nFin de la partie.\nLe mot était : " + word)
                self.game_running = False
                return
            else:
                answer = answer.content.upper()
                if answer in found_letters:
                    await self.bot.say("Vous avez déjà choisi cette lettre.")
                elif answer in word:
                    found_letters.append(answer)
                else:
                    remaining_tries -= 1
                revealedWord = get_revealed_word(word, found_letters)
            won, lost = evaluate_game(word, revealedWord, remaining_tries)
        if won:
            await self.bot.say("```Bien joué ! Le mot était : " + word + "```")
        else:
            await self.bot.say("```Vous êtes mauvais ! Le mot était : " + word + "```")
        self.game_running = False

def setup(bot):
    n = Game(bot)
    bot.add_cog(n)
