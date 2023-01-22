import discord
from button.StageButton import StageButton
from data import SqliteConnection
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
async def create_stage_message(ctx: discord.Interaction, rule: str):
    try:
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

        ruleId = SqliteConnection.get_rule_id(rule)
        stage_data = SqliteConnection.get_stage_data()
        for stageId, stage in stage_data:
            fname = f"stage{stageId}.png"
            file = discord.File(
                fp=f"./img/stage/{stage}.png", filename=fname, spoiler=False
            )
            embed = create_stage_embed(fname)

            message = await channel.send(
                file=file, embed=embed, view=StageButton(stage=stage)
            )

            thread = await message.create_thread(name=stage)
            embeds = []
            member = SqliteConnection.get_member_data(ctx.guild_id)
            files = []
            for playerId, player in member:
                # print(f"{ruleId}, {playerId}, {stageId}")
                fname = f"s_{stageId}_p_{playerId}.jpg"
                weaponData = SqliteConnection.get_formation_weapon_data_using_id(
                    ruleId, stageId, playerId
                )
                embeds.append(create_player_embed(player, weaponData, fname))
                if weaponData[0] != "未設定":
                    file = discord.File(
                        fp=f"./img/weapon/{weaponData[0]}.jpg",
                        filename=fname,
                        spoiler=False,
                    )
                    files.append(file)

            await thread.send(files=files, embeds=embeds)
            # for member in members:
            #     await thread.add_user(member)
    except Exception:
        raise
