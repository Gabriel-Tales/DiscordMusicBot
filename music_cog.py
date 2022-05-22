from ChannelState import channelState
from discord.ext import tasks, commands
from channel import Channel
from channelController import ChannelController

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.channelsController = ChannelController()
        self.CheckAFK.start()

    @commands.command(name="p")
    async def PlayMusic(self, ctx, *args):
        channelKey = ctx.author.voice.channel.id

        currentVoiceChannel = self.channelsController.GetChannel(channelKey)

        if(currentVoiceChannel == ""):
            currentVoiceChannel = Channel(ctx)
            
            self.channelsController.AddChannel(currentVoiceChannel)

        await currentVoiceChannel.connectChannel()

        await currentVoiceChannel.AddMusic(ctx, args)

        if(currentVoiceChannel.currentState == channelState.PLAYING):
            return

        currentVoiceChannel.StateMachine(channelState.PLAY)

    @commands.command(name="pause")
    async def pause(self, ctx):
        keyChannel = ctx.author.voice.channel.id
        currentChannel = self.channelsController.GetChannel(keyChannel)
        if(ctx.voice_client.is_paused()):
            await ctx.send(f"Resuming {currentChannel.musicQueue[0]['title']}")
        else:
            await ctx.send(f"Pausing {currentChannel.musicQueue[0]['title']}")
        currentChannel.StateMachine(channelState.PAUSE)
        
    #Disconnect bot with correct variables 
    @commands.command(name="disconnect", help="Disconnect from the actual voice channel")
    async def disconnect(self,ctx):
        if ctx.author.voice is None:
            await ctx.send("Im not in a channel ")
            return
        
        keyChannel = ctx.author.voice.channel.id
        self.channelsController.DeleteChannel(keyChannel)
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnecting")

    @commands.command(name="skip")
    async def skip(self, ctx):
        keyChannel = ctx.author.voice.channel.id
        currentChannel = self.channelsController.GetChannel(keyChannel)
        currentChannel.StateMachine(channelState.SKIP)

    @commands.command(name="queue")
    async def GetQueue(self, ctx):
        keyChannel = ctx.author.voice.channel.id
        currentChannel = self.channelsController.GetChannel(keyChannel)
        await currentChannel.GetQueue()


    @tasks.loop(seconds=150.0)
    async def CheckAFK(self):
        for channelLists in self.channelsController.channelHashtable:
            for channel in channelLists:
                if(channel):
                    if(channel.lastLoopState == channel.currentState == channelState.AFK):
                        if(channel):
                            keyChannel = channel.ctx.voice_client.channel.id
                        
                        else: return
                        
                        self.channelsController.DeleteChannel(keyChannel)
                        await channel.disconnectChannel()
                        return
                    channel.lastLoopState = channel.currentState
    
