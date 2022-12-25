from discord.ext import tasks
import discord
import os
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
from discord import Interaction

load_dotenv()

stageList = ["ゴンズイ地区", "スメーシーワールド", "キンメダイ美術館", 
            "マテガイ放水路", "マヒマヒリゾート&スパ", "海女美術大学",
            "ナメロウ金属", "チョウザメ造船", "ヤガラ市場", "ザトウマーケット", 
            "ユノハナ大渓谷", "マサバ海峡大橋", "ヒラメが丘団地", "クサヤ温泉"]

TOKEN = os.environ.get('TOKEN')
GUILD_ID = os.environ.get('GUILD_ID')

MY_GUILD = discord.Object(id=GUILD_ID)

result = dict(zip(stageList,[["ー", "ー"] for _ in stageList] ))
result["ゴンズイ地区"][0] = "〇"

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # self.tree.copy_global_to()
        await self.tree.sync()

intents = discord.Intents.all()  # Intentsオブジェクトを生成
client = MyClient(intents=intents)

class RegisterButton(discord.ui.View):
    def __init__(self, custom_id: str):
        super().__init__()
    
    @discord.ui.button(label = 'win')
    async def total_win (self, ctx: Interaction, button: discord.ui.Button):
        await ctx.response.send_message("win")

    @discord.ui.button(label = 'lose')
    async def total_lose (self, ctx: Interaction, button: discord.ui.Button):
        await ctx.response.send_message("lose")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.tree.command(name = "test", description = "test")
async def test(ctx: Interaction):
    await ctx.response.send_message(f'hello World')
    
@client.tree.command(name = "setup", description = "初期設定を行います")
async def setup(ctx: Interaction):
    await ctx.response.send_message(f'setup中')
    channel = await ctx.guild.create_text_channel("対抗戦記録")
    for stage in stageList:
        thread = await channel.create_thread(name = stage)
    
    embed = discord.Embed(color=0x00ff00)

    # embed.set_image(url="https://image.example.com/main.png") # 大きな画像タイルを設定できる

    # print("\n".join(stageList))
    for stage in stageList:
        embed.add_field(name=f"{stage}", value=f"|{'|'.join(result[stage])}|", inline=False) # フィールドを追加。
    # embed.add_field(name="", value=' - \n' * len(stageList), inline=True)

    await channel.send(embed=embed, view=RegisterButton(custom_id="total")) # embedの送信には、embed={定義したembed名}
    
    await ctx.followup.send(f'setup完了')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await message.channel.send('Hello!')


    
client.run(TOKEN)
