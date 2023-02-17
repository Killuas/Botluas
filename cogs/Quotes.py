import discord
import os
from discord.ext import commands
import json
import random

class Quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Quotes cog loaded")

    #Produces a quote that is stored in the json database
    @commands.command(name='quote', help='Returns a random quote or quote from a named person.')
    async def quote(self, ctx, name = None):
        guild = str(ctx.message.guild.id)
        quotes = json.load(open('./quotes/' + guild + '.json'))
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
    @commands.command(name='addquote', help='Adds a quote to the list. Name goes before quote.')
    @commands.has_role('Bot Admin')
    async def addquote(self, ctx, name, *, quote):
        newquote = {"name":name, "quote":quote}
        guildfile = './quotes/' + str(ctx.message.guild.id) + '.json'
        #checks if file exists and is readable, else create file
        if os.path.isfile(guildfile) and os.access(guildfile, os.R_OK):
            quotes = json.load(open(guildfile))
            quotelist = []
            for quote in quotes:
                quotelist.append({"name":quote['name'], "quote":quote['quote']})
            quotelist.append(newquote)
            with open(guildfile, 'w') as outfile:
                json.dump(quotelist, outfile, indent=4)
            await ctx.send(f"Quote #{len(quotelist)} successfully added")
        else:
            formattedquote = [newquote]
            with open(guildfile, 'w+') as outfile:
                json.dump(formattedquote, outfile, indent=4)
            await ctx.send (f"Quote #1 successfully added")
    #Errors for if addquote doesn't work
    @addquote.error
    async def addquote_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("You do not have the required role to use this command")
        else:
            await ctx.send("Unknown error, contact owner")

    #command to remove quote from json database
    @commands.command(name='delquote', help='Deletes a quote based on the number given.')
    @commands.has_role('Bot Admin')
    async def delquote(self, ctx, num):
        if int(num) < 1:
            await ctx.send("That is not a valid quote number")
            return
        guild = str(ctx.message.guild.id)
        quotes = json.load(open('./quotes/' + guild + '.json'))
        del quotes[int(num)-1]
        with open('./quotes/' + guild + '.json', 'w') as outfile:
            json.dump(quotes, outfile, indent=4)
        await ctx.send(f"Quote #{num} sucessfully deleted")
    #Errors for if delquote doesn't work
    @delquote.error
    async def delquote_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("You do not have the required role to use this command")
        else:
            await ctx.send(f"That is not a valid quote number")

#setup for the cog
async def setup(bot):
    await bot.add_cog(Quotes(bot))