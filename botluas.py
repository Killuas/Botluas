#Discord bot that I have created for my own discord server. Has several functions, including
#the ability to play sound clips when people join a voice channel and a roll function.
#Created by Iskander#0042 / https://github.com/Killuas/
import os
import discord
import asyncio
from dotenv import load_dotenv
from discord.ext import commands

def main():     
    #Defines intents for the bot to see
    intents = discord.Intents.default()
    intents.members = True
    intents.typing = True
    intents.message_content = True
    intents.presences = True

    # Decides the command prefix for the bot
    bot = commands.Bot(command_prefix='!', intents = intents)
    load_dotenv()
    #Loads the token for the bot from the .env file
    token = os.getenv('DISCORD_TOKEN')

    #Events that are performed when the bot starts up
    @bot.event
    async def on_ready():
        #sets the status to "Listening to !help"
        await bot.change_presence(activity=discord.Activity(type = 
        discord.ActivityType.listening, name='!help'))
        #announces when connected to discord
        print(f'{bot.user.name} has connected to Discord!')

    #load cogs then run them
    async def load_extensions():  
        for c in os.listdir("./cogs"):
            if c.endswith(".py"):
                await bot.load_extension("cogs." + c[:-3])
    asyncio.run(load_extensions())

    #Runs the bot
    bot.run(token)

main()