from discord.ext import commands
import discord
import json
import os

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Voice cog loaded")

    #Will play sound clips that are stored in the bots files, checking a json file to play them
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        #Voice clips to play when users join channels, mp3s go in VoiceClips folder
        voicepath = './VoiceClips/'+ str(member.guild.id) +'.json'
        if os.path.isfile(voicepath) and os.access(voicepath, os.R_OK):
            voiceclips = json.load(open(voicepath))
        else:
            return
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
            for vclient in self.bot.voice_clients:
                if vclient.channel == before.channel:
                    await vclient.disconnect()
        #Seeing if I can handle errors here, but I don't think so for now. Revisiting later.
        #@on_voice_state_update.error
        #async def on_voice_state_update_error(self, ctx, error):
        #    if isinstance(error, commands.BadArgument):
        #        await ctx.send("No file found")



#setup for the cog
async def setup(bot):
    await bot.add_cog(Voice(bot))