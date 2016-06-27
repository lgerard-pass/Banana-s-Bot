from discord.ext import commands
from client.constants import *
from client.games.hangman import *

class Game:
    def __init__(self, bot):
        self.bot = bot
        # Defining bot inner variables
        self.game_running = False

    def games_channel_check(ctx):
        if (ctx.message.channel.id != game_channel_id):
            return False
        else:
            return True

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
