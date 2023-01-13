import discord
from button.StageButton import StageButton
from data.ResultData import ResultData
from data.StageData import StageData

from logic.create_embed import (
    create_player_embed,
    create_result_embed,
    create_stage_embed,
)
from logic.utils import is_not_pined_message

# ルールボタンを押した際の処理
# TODO: フラグを設けてボタン押下後からfinを押すまで動作しないようにする
async def create_stage_message(ctx: discord.Interaction):
    channel = ctx.channel
    stage_list = StageData.get_stage_list()

    # 結果メッセージ(ピン止めされているメッセージ)以外を消去
    # TODO スレッドも削除
    await channel.purge(check=is_not_pined_message)

    await ctx.message.create_thread(name="全体")

    # 結果メッセージの内容を初期化
    ResultData.init_result()
    result_message = ResultData.get_result_message()
    embed = create_result_embed()
    await result_message.edit(embed=embed)

    for index, stage in enumerate(stage_list):
        fname = f"stage{index}.png"
        file = discord.File(
            fp=f"./img/stage/{stage}.png", filename=fname, spoiler=False
        )
        embed = create_stage_embed(fname)

        message = await channel.send(
            file=file, embed=embed, view=StageButton(stage=stage)
        )

        thread = await message.create_thread(name=stage)
        embeds = []
        for index in range(4):
            embeds.append(create_player_embed("test", f"weapon{index}"))
        await thread.send(embeds=embeds)
        # for member in members:
        #     await thread.add_user(member)
