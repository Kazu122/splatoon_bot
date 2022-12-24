import discord
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get('TOKEN')

intents = discord.Intents.default()  # デフォルトのIntentsオブジェクトを生成
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await message.channel.send('Hello!')

client.run(TOKEN)