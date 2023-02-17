from discord.ext import commands

class Errors(commands.Cog):
    def __init__(bot, self):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Errors cog loaded")

    #Errors that are raised to the user
    @commands.event
    async def on_command_error(self, ctx, error):
        #Will inform the user that the command they entered is not a command if it is not defined
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('That is not a command')
            return
        #Else return an error to the console
        raise error
    
#setup for the cog
async def setup(bot):
    await bot.add_cog(Errors(bot))