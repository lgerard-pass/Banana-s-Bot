from discord.ext import commands
import random

class Miscellaneous:
    """Miscellaneous commands"""
    def __init__(self, bot):
        self.bot = bot

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

def setup(bot):
    n = Miscellaneous(bot)
    bot.add_cog(n)