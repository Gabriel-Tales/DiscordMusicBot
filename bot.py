import discord
from discord.ext import commands


from music_cog import music_cog

Bot = commands.Bot("!")

Bot.add_cog(music_cog(Bot))

token = "discord Token"
        
Bot.run(token)