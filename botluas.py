#Discord bot that I have created for my own discord server. Has several functions, including
#the ability to play sound clips when people join a voice channel and a roll function.
#Created by Killuas#0042 / https://github.com/Killuas/
import os
import random
import discord
import json
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
    #Bot disconnects if the channel it is in is empty
    if after.channel is None and len(before.channel.members) == 1:
        for vclient in bot.voice_clients:
            if vclient.channel == before.channel:
                await vclient.disconnect()

#Errors that are raised to the user
@bot.event
async def on_command_error(ctx, error):
    #Will inform the user that the command they entered is not a command if it is not defined
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('That is not a command')
        return
    #Else return an error to the console
    raise error

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

#Produces a quote that is stored in the json database
@bot.command(name='quote', help='Choose a random quote from the database to produce, you can add a name at the end to specify a user you want the quote to be from')
async def quote(ctx, name = None):
    quotes = json.load(open('./quotes.json'))
    #Checks if the user chose to find a quote from a specific person
    if name is not None:
        namedquotes = []
        for person in quotes:
            if person["name"].lower() == name.lower():
                namedquotes.append(person)
        quotes = namedquotes
    #Checks to make sure that the user who was named is in the database
    if not quotes:
        await ctx.send(f"There are no quotes from {name}")
        return
    quotenum = random.randint(0, len(quotes)-1)
    name = quotes[quotenum]["name"]
    quote = quotes[quotenum]["quote"]
    await ctx.send(f"\"{quote}\" -{name}")

#Command to add a new quote to the bots json database
@bot.command(name='addquote', help='Adds a quote to the database, requires you to name a user first then input the quote')
@commands.has_role('Bot Admin')
async def addquote(ctx, name, *, quote):
    newquote = {"name":name, "quote":quote}
    quotes = json.load(open('./quotes.json'))
    quotelist = []
    for quote in quotes:
        quotelist.append({"name":quote['name'], "quote":quote['quote']})
    quotelist.append(newquote)
    with open('./quotes.json', 'w') as outfile:
        json.dump(quotelist, outfile, indent=4)
    await ctx.send(f"Quote #{len(quotelist)} successfully added")
@addquote.error
async def addquote_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have the required role to use this command")

@bot.command(name='delquote', help='Deletes the quote numbered what the user enters. This changes the number of all quotes after the deleted quote.')
@commands.has_role('Bot Admin')
async def delquote(ctx, num):
    if int(num) < 1:
        await ctx.send("That is not a valid quote number")
        return
    quotes = json.load(open('./quotes.json'))
    del quotes[int(num)-1]
    with open('./quotes.json', 'w') as outfile:
        json.dump(quotes, outfile, indent=4)
    await ctx.send(f"Quote #{num} sucessfully deleted")
@delquote.error
async def delquote_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have the required role to use this command")
    else:
        await ctx.send(f"That is not a valid quote number")

#Joke command I am going to remove on release
@bot.command(name='osur')
async def osur(ctx):
    await ctx.send(f"Dubs and osurs gay: {random.randint(1, 100)}")

#Runs the bot
bot.run(token)