import discord
from data.StageData import StageData
from data.ResultData import ResultData

# 結果記録用のembedを生成
def create_result_embed():
    embed = discord.Embed(color=0x00FF00)
    result = ResultData.get_result()
    for stage in StageData.get_stage_list():
        embed.add_field(
            name=f"{stage}", value=f"|{'|'.join(result[stage])}|", inline=False
        )

    return embed


# ステージ画像のembedを作成
def create_stage_embed(fname: str):
    embed = discord.Embed(color=0x00FF00)
    embed.set_image(url=f"attachment://{fname}")

    return embed


def create_player_embed(player: str, WeaponData: list[str, str, str], fname: str):
    embed = discord.Embed(title=player, color=0x00FF00)
    # print(WeaponData)
    name, sub, special = WeaponData
    if name != "未設定":
        embed.set_thumbnail(url=f"attachment://{fname}")

    embed.add_field(name=name, value=f"  {sub}\n  {special}")

    return embed


def create_archive_embed(message: discord.Message):
    author = message.author.name
    content = message.content
    embed = discord.Embed(color=0x00FF00)
    embed.set_author(name=author)
    day = "{0: %Y/%m%d}".format(message.created_at)
    embed.add_field(name=day, value=content)

    return embed
