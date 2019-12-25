#Discord bot that I have created for my own discord server. Has several functions, including
#the ability to play sound clips when people join a voice channel and a roll function.
#Created by Killuas#0042 / 
import os
import random
import discord
import json
import asyncio
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
#Loads the token for the bot from the .env file
token = os.getenv('DISCORD_TOKEN')
#Voice clips to play when users join channels, mp3s go in VoiceClips folder
voiceclips = json.load(open('./VoiceClips/voiceclips.json'))

# Decides the command prefix for the bot
bot = commands.Bot(command_prefix='!')

#Events that are performed when the bot starts up
@bot.event
async def on_ready():
    #sets the status to "Listening to !help"
    await bot.change_presence(activity=discord.Activity(type = 
    discord.ActivityType.listening, name='!help'))
    #announces when connected to discord
    print(f'{bot.user.name} has connected to Discord!')

#Will play sound clips that are stored in the bots files, checking a json file to play them
@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        for user in voiceclips:
            if int(user['userid']) == member.id:
                print(f"{user['userid']} joined {after.channel.name} in {after.channel.guild.name}, playing {user['file']}")
                #Checks if there is currently a voice client active for the guild
                if member.guild.voice_client is None:
                    vc = await after.channel.connect()
                else:
                    vc = member.guild.voice_client
                    await vc.move_to(after.channel)
                vc.play(discord.FFmpegPCMAudio(f"./VoiceClips/{user['file']}"), after=lambda e:None)
                #Waits until sound clip finishes playing
                while vc.is_playing():
                    await asyncio.sleep(1)
    #Bot disconnects if the channel it is in is empty
    if after.channel is None and len(before.channel.members) == 1:
        for vclient in bot.voice_clients:
            if vclient.channel == before.channel:
                await vclient.disconnect()

#Command that produces the anti-bully ranger picture
@bot.command(name='nobully', help='Responds with the no bully picture')
async def nobully(ctx):
    await ctx.send(file=discord.File('./pictures/nobully.jpg'))

#Command that produces the Momiji awoo picture
@bot.command(name='awoo', help='Responds with the Momiji awoo picture')
async def awoo(ctx):
    await ctx.send(file=discord.File('./pictures/awoo.jpg'))

#Rolls an X sided dice, that defaults to 2 sides if no additional attribute is given
@bot.command(name='roll', help='Rolls a dice with X sides, default is 2 sides')
async def roll(ctx, atr=2):
        await ctx.send(random.randint(1, int(atr)))
@roll.error
async def roll_error(ctx, error):
    await ctx.send('Bad argument entered, input only integers greater than 0')

#Joke command I am going to remove on release
@bot.command(name='osur')
async def osur(ctx):
    await ctx.send(f"Dubs and osurs gay: {random.randint(1, 100)}")

bot.run(token)