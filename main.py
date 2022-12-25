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
from data.global_data import result
from data.global_data import resultMessage

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
    await ctx.response.send_message(f"hello World")


@client.tree.command(name="setup", description="初期設定を行います")
async def setup(ctx: Interaction):
    await ctx.response.send_message(f"setup中")
    channel = await ctx.guild.create_text_channel("対抗戦記録")
    members = channel.guild.members
    for stage in stage_list:
        thread = await channel.create_thread(name=stage)
        for member in members:
            await thread.add_user(member)
        embed = discord.Embed(color=0x00FF00)
        fname = f"{stage}.png"
        file = discord.File(fp=f"./img/{fname}", filename=fname)
        embed.set_image(url=f"attachment://{fname}")
        # embed.set_image(url=f"https://cdn.discordapp.com/embed/avatars/0.png")
        await thread.send(file=file, view=StageButton(stage=stage))

    embed = discord.Embed(color=0x00FF00)

    for stage in stage_list:
        embed.add_field(
            name=f"{stage}", value=f"|{'|'.join(result[stage])}|", inline=False
        )

    result_message = await channel.send(embed=embed, view=RegisterButton())
    resultMessage.set_result_message(result_message)

    await ctx.followup.send(f"setup完了")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await message.channel.send("Hello!")


client.run(TOKEN)
