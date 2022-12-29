import discord
from data.global_data import stage_list
from data.global_data import DataStore


def create_result_embed():
    embed = discord.Embed(color=0x00FF00)
    result = DataStore.get_result()
    for stage in stage_list:
        embed.add_field(
            name=f"{stage}", value=f"|{'|'.join(result[stage])}|", inline=False
        )

    return embed


def create_stage_embed(fname: str):
    embed = discord.Embed(color=0x00FF00)
    embed.set_image(url=f"attachment://{fname}")
    print(embed.image)

    return embed
