import discord
from youtube_dl import YoutubeDL
from ChannelState import channelState

class Channel:
    def __init__(self, ctx):
        
        # Configs ydl e ffmpeg
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        
        self.ctx = ctx
        self.musicQueue = []
        
        self.currentState = channelState.DISCONNECTED
        self.lastLoopState = self.currentState


    async def connectChannel(self):
        if(self.ctx.voice_client == None):
            await self.ctx.author.voice.channel.connect()
            self.StateMachine(channelState.AFK)

    async def disconnectChannel(self):
        if(self.ctx.voice_client != None):
            await self.ctx.voice_client.disconnect()

    def PlayMusic(self):
        if(self.currentState == channelState.PLAYING):
            return

        self.ctx.voice_client.play(discord.FFmpegPCMAudio(self.musicQueue[0]["source"], **self.FFMPEG_OPTIONS), after= lambda e: self.CheckNextMusic())
        self.StateMachine(channelState.PLAYING)
        
    #searching the item on youtube
    def search_yt(self, item):
        item = " ".join(item)
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception: 
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}


    def StateMachine(self, newState):
        self.currentState = newState
        
        if(self.currentState == channelState.PLAY):
            self.PlayMusic()
        
        elif(self.currentState == channelState.PAUSE):
            self.PauseMusic()
        
        elif(self.currentState == channelState.SKIP):
            self.SkipMusic()

    def PauseMusic(self):
        if(self.ctx.voice_client.is_paused()):
            self.ctx.voice_client.resume()
            self.StateMachine(channelState.PLAYING)
        else:
            self.ctx.voice_client.pause()

    async def AddMusic(self, ctx, query):
        song = self.search_yt(query)
        self.musicQueue.append(song)
        await ctx.send(f"Music Added: {song['title']}")
                
    #bug
    def CheckNextMusic(self):
        if(len(self.musicQueue) > 1):
            self.musicQueue.pop(0)
            self.StateMachine(channelState.PLAY)
            
        elif (len(self.musicQueue) == 1):
            self.musicQueue.pop(0)
            self.StateMachine(channelState.AFK)

    def SkipMusic(self):
        #Por conta da função after do .play, ao parar a musica já é execitadp p checkNextMusic()
        self.ctx.voice_client.stop()

    async def GetQueue(self):
        title = ""#f"{self.musicQueue[0]['title']}"
        for i, song in enumerate(self.musicQueue):
            title += f"{i+1}: {song['title']}\n"
        
        await self.ctx.send(title)


        
        