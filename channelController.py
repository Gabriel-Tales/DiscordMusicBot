
class ChannelController:
    def __init__(self):
        self.hashSize = 20
        self.channelHashtable = [[] for i in range(self.hashSize)]

    def AddChannel(self, channelObj):
        index = self.CalculateHash(channelObj.ctx.author.voice.channel.id)
        self.channelHashtable[index].append(channelObj)

    def CalculateHash(self, key):
        hash = 5381
        hash = ((hash << 5)+ hash) + key
        index = hash % self.hashSize
        return index
    
    def GetChannel(self, key):
        channelList = self.channelHashtable[self.CalculateHash(key)]

        for channel in channelList:
            if(channel.ctx.voice_client.channel.id == key):
                return channel
        return ""

    def DeleteChannel(self, key):
        channelList = self.channelHashtable[self.CalculateHash(key)]

        for channel in channelList:
            if(channel.ctx.voice_client.channel.id == key):
                channelList.remove(channel)
    
