import discord
from discord.ext import commands


from music_cog import music_cog

Bot = commands.Bot("!")

Bot.add_cog(music_cog(Bot))

token = "ODg4MTAzNDA5NDg2NTI4NTYz.YUN0wA.fgNkcqSkz95mLw5ssxsmrtnPAB8"
        
Bot.run(token)