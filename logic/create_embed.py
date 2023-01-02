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


def create_player_embed(player: str, fname: str):
    embed = discord.Embed(title=player, color=0x00FF00)
    embed.add_field(name="weapon", value="  sub weapon\n  special weapon")
    embed.set_thumbnail(url=f"attachment://{fname}")

    return embed
