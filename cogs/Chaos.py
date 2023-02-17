from discord.ext import commands
import random

class Chaos(commands.Cog, name = "Random"):
    def __init__(self, bot):
         self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Random cog loaded")

    #Rolls an X sided dice, that defaults to 2 sides if no additional attribute is given
    @commands.command(name = 'roll', help = 'Rolls a dice with X sides, default is 2 sides.')
    async def roll(self, ctx, atr=2):
            await ctx.send(random.randint(1, int(atr)))
    @roll.error
    async def roll_error(self, ctx, error):
        await ctx.send('Bad argument entered, input only integers greater than 0')

    #Flips a coin
    @commands.command(name = 'coinflip', help = 'Flips a coin that shows heads or tails.')
    async def coinflip(self, ctx):
        coin = random.randint(0, 1)
        if coin == 0:
            await ctx.send('Heads')
        else:
            await ctx.send('Tails')

#setup for the cog
async def setup(bot):
    await bot.add_cog(Chaos(bot))