from discord.ext import tasks
import discord
import os
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

load_dotenv()

TOKEN = os.environ.get('TOKEN')
GUILD_ID = os.environ.get('GUILD_ID')

MY_GUILD = discord.Object(id=GUILD_ID)

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # self.tree.copy_global_to()
        await self.tree.sync()

intents = discord.Intents.all()  # Intentsオブジェクトを生成
client = MyClient(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.tree.command(name = "test", description = "test")
async def test(ctx):
    await ctx.response.send_message(f'hello World')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await message.channel.send('Hello!')

client.run(TOKEN)
