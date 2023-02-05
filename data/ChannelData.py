class ChannelData:

    _channels = {}

    # DBに毎回アクセスする必要がないように保持しておく
    _channelType = {"category": 1, "text": 2, "voice": 3, "thread": 4}

    @classmethod
    def get_channels(cls):
        return cls._channels

    @classmethod
    def set_channels(cls, channels):
        cls._channels = channels

    # チャンネルタイプのIDを取得する
    @classmethod
    def get_channel_type(cls, kind: str):
        return cls._channelType[kind]
