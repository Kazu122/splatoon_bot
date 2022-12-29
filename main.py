from discord.ext import tasks
import discord
import os
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
from discord import Interaction
from button.RegisterButton import RegisterButton
from button.StageButton import StageButton
from data.global_data import stage_list
from data.global_data import DataStore
from logic.create_embed import create_stage_embed
from spreadsheet.connect_sheet import OperateSpreadSheet

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

# TODO: チャンネルが存在する場合に取得してresult_messageをセットする
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.tree.command(name="test", description="test")
async def test(ctx: Interaction):
    OperateSpreadSheet.set_result_data()
    await ctx.response.send_message(f"hello World")


@client.tree.command(name="setup", description="初期設定を行います")
async def setup(ctx: Interaction):
    await ctx.response.send_message(f"setup中")
    channel = await ctx.guild.create_text_channel("対抗戦記録")
    members = channel.guild.members
    embed = discord.Embed(color=0x00FF00)
    result = DataStore.get_result()

    # 記録用embedを生成
    for stage in stage_list:
        embed.add_field(
            name=f"{stage}", value=f"|{'|'.join(result[stage])}|", inline=False
        )

    result_message = await channel.send(embed=embed, view=RegisterButton())
    DataStore.set_result_message(result_message)

    for index, stage in enumerate(reversed(stage_list)):
        thread = await channel.create_thread(name=stage)
        for member in members:
            await thread.add_user(member)
        fname = f"stage{index}.png"
        file = discord.File(
            fp=f"./img/stage/{stage}.png", filename=fname, spoiler=False
        )
        embed = create_stage_embed(fname)
        await thread.send(file=file, embed=embed, view=StageButton(stage=stage))

    await ctx.followup.send(f"setup完了")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await message.channel.send("Hello!")


client.run(TOKEN)
