from typing import Sequence
import discord
from discord import CategoryChannel, Guild, Interaction, Member, TextChannel
from data.StageData import StageData
from button.RegisterButton import RegisterButton
from button.StageButton import StageButton
from data.ResultData import StageData
from data.ResultData import ResultData
from logic.create_embed import create_player_embed, create_stage_embed
from logic.utils import is_not_pined_message


def get_category_id(category_ids: dict, name: str):
    if name in category_ids:
        return category_ids[name]["id"]

    # keyにnameが存在しない場合は追加する
    category_ids[name] = {"id": None, "channels": {}}
    return None


# channel_idsにはテキストチャンネルの辞書を渡すこと
def get_text_channel_id(channel_ids: dict, name: str):
    if name in channel_ids:
        return channel_ids[name]["id"]

    # keyにnameが存在しない場合は追加する
    channel_ids[name] = {"id": None, "messages": {}, "threads": {}}
    return None


# thread_idにはスレッドの辞書を渡すこと
def get_thread_id(thread_ids: dict, name: str):
    if name in thread_ids:
        return thread_ids[name]["id"]

    return None


def get_message_id(message_ids: dict, name: str):
    if name in message_ids:
        return message_ids[name]["id"]

    return None


# TODO ファイルが存在しない場合にも動くようにする(keyError 対策を行う)
async def create_main_channel(
    guild: Guild, members: Sequence[Member], channel_ids: dict
):

    category = guild.get_channel(get_category_id(channel_ids, "対抗戦記録用"))
    # 存在しない場合はカテゴリを生成
    if category == None:
        category = await guild.create_category("対抗戦記録用")
    channels = {}
    dict = {"id": category.id, "channels": channels}

    stage_list = StageData.get_stage_list()
    channel = guild.get_channel(
        get_text_channel_id(channel_ids["対抗戦記録用"]["channels"], "対抗戦記録")
    )

    embed = discord.Embed(color=0x00FF00)
    result = ResultData.get_result()

    # 記録用embedを生成
    for stage in stage_list:
        embed.add_field(
            name=f"{stage}", value=f"|{'|'.join(result[stage])}|", inline=False
        )
    # 存在しない場合はテキストチャンネルを生成
    if channel == None:
        channel = await category.create_text_channel("対抗戦記録")
    else:
        await channel.purge()

    result_message = await channel.send(embed=embed, view=RegisterButton())
    await result_message.pin()
    ResultData.set_result_message(result_message)

    channels[channel.name] = {
        "id": channel.id,
        "messages": {},
        "threads": {},
    }

    return dict


async def create_data_channel(
    guild: Guild, members: Sequence[Member], channel_ids: dict
):
    category = guild.get_channel(get_category_id(channel_ids, "データ"))
    if category == None:
        category = await guild.create_category("データ")

    dict = {"id": category.id, "channels": {}}

    # チャンネル名のリスト
    channel_list = ["勝率推移", "マップ", "武器", "編成", "リンク"]

    for name in channel_list:
        if name == "武器":
            channel = guild.get_channel(
                get_text_channel_id(channel_ids["データ"]["channels"], name)
            )
            if channel == None:
                channel = await category.create_text_channel(name)
        else:
            channel = guild.get_channel(
                get_text_channel_id(channel_ids["データ"]["channels"], name)
            )
            if channel == None:
                channel = await category.create_text_channel(name)

        dict["channels"][channel.name] = {
            "id": channel.id,
            "messages": {},
            "threads": {},
        }

    return dict


async def create_archive_channel(
    guild: Guild, members: Sequence[Member], channel_ids: dict
):
    category = guild.get_channel(get_category_id(channel_ids, "アーカイブ"))
    if category == None:
        category = await guild.create_category("アーカイブ")

    channels = {}
    dict = {"id": category.id, "channels": channels}

    stage_list = StageData.get_stage_list()
    resultChannel = guild.get_channel(
        get_text_channel_id(channel_ids["アーカイブ"]["channels"], "対抗戦結果")
    )
    if resultChannel == None:
        resultChannel = await category.create_text_channel("対抗戦結果")
    channels["対抗戦結果"] = {"id": resultChannel.id, "messages": {}, "threads": {}}

    introspectionChannel = guild.get_channel(
        get_text_channel_id(channel_ids["アーカイブ"]["channels"], "対抗戦反省")
    )
    if introspectionChannel == None:
        introspectionChannel = await category.create_text_channel("対抗戦反省")
    threads = {}
    channels["対抗戦反省"] = {
        "id": introspectionChannel.id,
        "messages": {},
        "threads": threads,
    }

    # ResultData.set_result_message(result_message)

    thread = None
    thread_id = get_thread_id(
        channel_ids["アーカイブ"]["channels"]["対抗戦反省"]["threads"], "全体"
    )

    try:
        thread = await guild.fetch_channel(thread_id)
    except (discord.NotFound, discord.InvalidData, discord.HTTPException):
        # idがNoneまたはチャンネルが見つからなかった場合なにもしない
        pass
    # 存在しない場合全体反省用のスレッドを生成
    if thread == None:
        thread = await introspectionChannel.create_thread(name="全体")

    threads["全体"] = {"id": thread.id}

    for stage in reversed(stage_list):
        thread = None
        thread_id = get_thread_id(
            channel_ids["アーカイブ"]["channels"]["対抗戦反省"]["threads"], stage
        )

        try:
            thread = await guild.fetch_channel(thread_id)
        except (discord.NotFound, discord.InvalidData, discord.HTTPException):
            # idがNoneまたはチャンネルが見つからなかった場合なにもしない
            pass
        # 存在しない場合全体反省用のスレッドを生成
        if thread == None:
            thread = await introspectionChannel.create_thread(name=stage)
            # for member in members:
            #     await thread.add_user(member)
        threads[stage] = {"id": thread.id, "messages": {}}

    return dict


async def create_document_channel(
    guild: Guild, members: Sequence[Member], channel_ids: dict
):
    category = guild.get_channel(get_category_id(channel_ids, "ドキュメント"))
    if category == None:
        category = await guild.create_category("ドキュメント")

    dict = {"id": category.id, "channels": {}}

    # チャンネル名のリスト
    channel_list = ["使い方", "更新情報"]

    for name in channel_list:
        channel = guild.get_channel(
            get_text_channel_id(channel_ids["ドキュメント"]["channels"], name)
        )
        if channel == None:
            channel = await category.create_text_channel(name)

        dict["channels"][name] = {"id": channel.id, "messages": {}, "threads": {}}

    return dict


async def create_management_channel(
    guild: Guild, members: Sequence[Member], channel_ids: dict
):
    category = guild.get_channel(get_category_id(channel_ids, "管理用"))
    if category == None:
        category = await guild.create_category("管理用")
    dict = {"id": category.id, "channels": {}}

    # チャンネル名のリスト
    channel_list = ["コマンド", "ログ"]

    for name in channel_list:
        channel = guild.get_channel(
            get_text_channel_id(channel_ids["管理用"]["channels"], name)
        )
        if channel == None:
            channel = await category.create_text_channel(name)

        dict["channels"][name] = {"id": channel.id, "messages": {}, "threads": {}}

    return dict
