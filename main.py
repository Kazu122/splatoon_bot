import discord
import os
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

load_dotenv()

TOKEN = os.environ.get('TOKEN')

intents = discord.Intents.all()  # Intentsオブジェクトを生成
client = discord.Client(intents=intents, command_prefix='/')
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await tree.sync()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await message.channel.send('Hello!')

@tree.command(name = 'test', description='test')
async def test(interaction):
    await interaction.response.send_message(f'hello world')
    
@slash.slash(name="test")

async def _test(ctx: SlashContext):

    embed = discord.Embed(title="embed test")

    await ctx.send(content="test", embeds=[embed])

client.run(TOKEN)
