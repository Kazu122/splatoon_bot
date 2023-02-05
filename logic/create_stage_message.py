import discord
from button.StageButton import StageButton
from data import SqliteConnection
from data.ChannelData import ChannelData
from data.ResultData import ResultData
from data.StageData import StageData

from logic.create_embed import (
    create_player_embed,
    create_result_embed,
    create_stage_embed,
)
from logic.utils import is_not_pined_message
from spreadsheet.connect_sheet import OperateSpreadSheet

# ルールボタンを押した際の処理
# TODO: フラグを設けてボタン押下後からfinを押すまで動作しないようにする
async def create_stage_message(ctx: discord.Interaction, rule: str):
    try:
        channel = ctx.channel

        # 全期間の集計データ
        d = OperateSpreadSheet.get_all_term_data()
        totalizeData = {
            array[0]: {"win": int(array[1]), "lose": int(array[2])} for array in d
        }

        # 今月の集計データ
        d = OperateSpreadSheet.get_recently_data()
        monthlyData = None
        if d != None:
            monthlyData = {
                array[0]: {"win": int(array[1]), "lose": int(array[2])} for array in d
            }

        # 結果メッセージ(ピン止めされているメッセージ)以外を消去
        for thread in ctx.channel.threads:
            await thread.delete()
        await channel.purge(check=is_not_pined_message)

        # アーカイブチャンネルの取得
        type = ChannelData.get_channel_type("text")
        archiveId = SqliteConnection.get_channel(ctx.guild_id, "対抗戦反省", type)
        archive = ctx.guild.get_channel(archiveId)
        archiveThreads = {thread.name: thread for thread in archive.threads}

        overallThread = await ctx.message.create_thread(name="全体")
        overallArchive = archiveThreads["全体"]
        messages = [message async for message in overallArchive.history(limit=3)]
        for message in messages:
            await overallThread.send(embeds=message.embeds)

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
            # embed = create_stage_embed(fname)
            message = await channel.send(file=file, view=StageButton(stage=stage))

            thread = await message.create_thread(name=stage)
            embeds = []
            member = SqliteConnection.get_member_data(ctx.guild_id)
            files = []

            embed = discord.Embed(title="戦績", color=0x00FF00)
            win = totalizeData[stage]["win"]
            lose = totalizeData[stage]["lose"]
            win_rate = round(win / (win + lose), 2)
            embed.add_field(name="全期間", value=f"勝率: {win_rate}%({win}勝{lose}敗)")
            if monthlyData != None:
                win = monthlyData[stage]["win"]
                lose = monthlyData[stage]["lose"]
                win_rate = round(win / (win + lose), 2)
            else:
                win = "-"
                lose = "-"
                win_rate = "-"
            embed.add_field(name="今月", value=f"勝率: {win_rate}%({win}勝{lose}敗)")
            embeds.append(embed)
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

            baseThread = archiveThreads[stage]
            messages = [message async for message in baseThread.history(limit=3)]
            for message in messages:
                await thread.send(embeds=message.embeds)
    except Exception:
        raise
