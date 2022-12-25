import discord
from ..data.global_data import stage_list
from ..data.global_data import result


def create_result_embed():
    embed = discord.embed
    for stage in stage_list:
        embed.add_field(
            name=f"{stage}", value=f"|{'|'.join(result[stage])}|", inline=False
        )
