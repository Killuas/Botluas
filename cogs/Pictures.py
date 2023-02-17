import discord
from discord.ext import commands

class Pictures(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Pictures cog loaded")

    #Command that produces the anti-bully ranger picture
    @commands.command(name = 'nobully', help='Responds with the no bully picture')
    async def nobully(self, ctx):
        await ctx.send(file=discord.File('./pictures/nobully.jpg'))

    #Command that produces the Momiji awoo picture
    @commands.command(name = 'awoo', help='Responds with the Momiji awoo picture')
    async def awoo(self, ctx):
        await ctx.send(file=discord.File('./pictures/awoo.jpg'))

#setup for the cog
async def setup(bot):
    await bot.add_cog(Pictures(bot))