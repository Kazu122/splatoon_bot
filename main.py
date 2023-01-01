from discord.ext import tasks
import discord
import os
import json
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
from discord import Interaction
from logic.create_channel import *

load_dotenv()

TOKEN = os.environ.get("TOKEN")
GUILD_ID = os.environ.get("GUILD_ID")

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

# サーバーの初期化を行う
# TODO チャンネルが存在する場合は生成処理スキップ
async def init(guild: Guild):
    server_structure = {}

    if not (os.path.exists("./channelIds.json")):
        with open("./channelIds.json", "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=4)

    with open("./channelIds.json", "r", encoding="utf-8") as f:
        channel_ids = json.load(f)
        members = guild.members

        server_structure["対抗戦記録用"] = await create_main_channel(
            guild, members, channel_ids
        )
        server_structure["データ"] = await create_data_channel(guild, members, channel_ids)
        server_structure["アーカイブ"] = await create_archive_channel(
            guild, members, channel_ids
        )
        server_structure["ドキュメント"] = await create_document_channel(
            guild, members, channel_ids
        )
        server_structure["管理用"] = await create_management_channel(
            guild, members, channel_ids
        )

        print(server_structure)

    with open("./channelIds.json", "w", encoding="utf-8") as f:
        json.dump(server_structure, f, ensure_ascii=False, indent=4)


# TODO: チャンネルが存在する場合に取得してresult_messageをセットする
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    # TODO 起動時も初期化を行う
    guilds = client.guilds
    for guild in guilds:
        await init(guild)

    print("initialized complete")


# testコマンド: テスト用
@client.tree.command(name="test", description="test")
async def test(ctx: Interaction):
    await ctx.response.send_message(f"hello World")


# setupコマンド: サーバーの初期設定を行う
@client.tree.command(name="setup", description="初期設定を行います")
async def setup(ctx: Interaction):
    await ctx.response.send_message(f"setup中")
    init(ctx.guild)
    await ctx.followup.send(f"setup完了")


@client.tree.command(name="clear", description="チャンネルをすべて削除します")
async def clear(ctx: Interaction):
    channels = await ctx.guild.fetch_channels()
    for channel in channels:
        await channel.delete()

    await ctx.guild.create_text_channel("command")
    await ctx.guild.create_voice_channel("test")


# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     await message.channel.send("Hello!")


client.run(TOKEN)
