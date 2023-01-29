from typing import Sequence
import discord
from discord import CategoryChannel, Guild, Interaction, Member, TextChannel
from data.ChannelData import ChannelData
from data.SqliteConnection import SqliteConnection
from data.StageData import StageData
from button.RegisterButton import SelectRuleButton
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
async def create_main_channel(guild: Guild, members: Sequence[Member]):
    categoryType = ChannelData.get_channel_type("category")
    textChannelType = ChannelData.get_channel_type("text")
    # ----- 記録用カテゴリ作成 -----
    categoryId = SqliteConnection.get_channel(guild.id, "対抗戦記録用", categoryType)
    category = None
    isInsert = True
    if categoryId != None:
        isInsert = False
        category = guild.get_channel(categoryId)

    # 存在しない場合はカテゴリを生成
    if category == None:
        category = await guild.create_category("対抗戦記録用")
        SqliteConnection.set_channel(
            guild.id, category.id, categoryType, "対抗戦記録用", isInsert=isInsert
        )

    # ----- 記録用チャンネル作成 -----
    stage_list = StageData.get_stage_list()
    channelId = SqliteConnection.get_channel(guild.id, "対抗戦記録", textChannelType)
    channel = None
    isInsert = True
    if channelId != None:
        isInsert = False
        channel = guild.get_channel(channelId)

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
        SqliteConnection.set_channel(
            guild.id, channel.id, textChannelType, "対抗戦記録", isInsert=isInsert
        )
    else:
        await channel.purge()

    result_message = await channel.send(embed=embed, view=SelectRuleButton())
    await result_message.pin()
    ResultData.set_result_message(result_message)

    return


async def create_data_channel(guild: Guild, members: Sequence[Member]):
    categoryType = ChannelData.get_channel_type("category")
    textChannelType = ChannelData.get_channel_type("text")
    categoryId = SqliteConnection.get_channel(guild.id, "データ", categoryType)
    category = None
    isInsert = True
    if categoryId != None:
        isInsert = False
        category = guild.get_channel(categoryId)

    if category == None:
        category = await guild.create_category("データ")
        SqliteConnection.set_channel(
            guild.id, category.id, categoryType, "データ", isInsert=isInsert
        )

    # チャンネル名のリスト
    channel_list = ["勝率推移", "マップ", "武器", "編成", "リンク"]

    for name in channel_list:
        isInsert = True
        channelId = SqliteConnection.get_channel(guild.id, name, textChannelType)
        channel = None
        if channelId != None:
            isInsert = False
            channel = guild.get_channel(channelId)
        if channel == None:
            channel = await category.create_text_channel(name)
            SqliteConnection.set_channel(
                guild.id, channel.id, textChannelType, name, isInsert=isInsert
            )

    return


async def create_archive_channel(guild: Guild, members: Sequence[Member]):
    categoryType = ChannelData.get_channel_type("category")
    textChannelType = ChannelData.get_channel_type("text")
    threadType = ChannelData.get_channel_type("thread")
    categoryId = SqliteConnection.get_channel(guild.id, "アーカイブ", categoryType)
    category = None
    isInsert = True
    if categoryId != None:
        isInsert = False
        category = guild.get_channel(categoryId)

    if category == None:
        category = await guild.create_category("アーカイブ")
        SqliteConnection.set_channel(
            guild.id, category.id, categoryType, "アーカイブ", isInsert=isInsert
        )

    stage_list = StageData.get_stage_list()

    resultId = SqliteConnection.get_channel(guild.id, "対抗戦結果", textChannelType)
    resultChannel = None
    isInsert = True
    if resultId != None:
        isInsert = False
        resultChannel = guild.get_channel(resultId)

    if resultChannel == None:
        resultChannel = await category.create_text_channel("対抗戦結果")
        SqliteConnection.set_channel(
            guild.id, resultChannel.id, textChannelType, "対抗戦結果", isInsert=isInsert
        )

    introspectionChannelId = SqliteConnection.get_channel(
        guild.id, "対抗戦反省", textChannelType
    )
    introspectionChannel = None
    isInsert = True
    if introspectionChannelId != None:
        isInsert = False
        introspectionChannel = guild.get_channel(introspectionChannelId)

    if introspectionChannel == None:
        introspectionChannel = await category.create_text_channel("対抗戦反省")
        SqliteConnection.set_channel(
            guild.id,
            introspectionChannel.id,
            textChannelType,
            "対抗戦反省",
            isInsert=isInsert,
        )
    # ResultData.set_result_message(result_message)

    thread = None
    thread_id = SqliteConnection.get_channel(guild.id, "全体", threadType)
    isInsert = True
    if thread_id != None:
        isInsert = False
        try:
            thread = await guild.fetch_channel(thread_id)
        except (discord.NotFound, discord.InvalidData, discord.HTTPException):
            # idがNoneまたはチャンネルが見つからなかった場合なにもしない
            pass

    # 存在しない場合全体反省用のスレッドを生成
    if thread == None:
        thread = await introspectionChannel.create_thread(name="全体")
        SqliteConnection.set_channel(
            guild.id, category.id, categoryType, "全体", isInsert=isInsert
        )

    for stage in reversed(stage_list):
        thread = None
        isInsert = True
        thread_id = SqliteConnection.get_channel(guild.id, stage, threadType)
        if thread_id != None:
            try:
                isInsert = False
                thread = await guild.fetch_channel(thread_id)
            except (discord.NotFound, discord.InvalidData, discord.HTTPException):
                # idがNoneまたはチャンネルが見つからなかった場合なにもしない
                pass
        # 存在しない場合ステージごと反省用のスレッドを生成
        if thread == None:
            thread = await introspectionChannel.create_thread(name=stage)
            # for member in members:
            #     await thread.add_user(member)
            SqliteConnection.set_channel(
                guild.id, category.id, categoryType, stage, isInsert=isInsert
            )

    return


async def create_document_channel(guild: Guild, members: Sequence[Member]):
    categoryType = ChannelData.get_channel_type("category")
    textChannelType = ChannelData.get_channel_type("text")
    categoryId = SqliteConnection.get_channel(guild.id, "ドキュメント", categoryType)
    category = None
    isInsert = True
    if categoryId != None:
        isInsert = False
        category = guild.get_channel(categoryId)

    if category == None:
        category = await guild.create_category("ドキュメント")
        SqliteConnection.set_channel(
            guild.id, category.id, categoryType, "ドキュメント", isInsert=isInsert
        )

    # チャンネル名のリスト
    channel_list = ["使い方", "更新情報"]

    for name in channel_list:
        channelId = SqliteConnection.get_channel(guild.id, name, textChannelType)
        isInsert = True
        channel = None
        if channelId != None:
            isInsert = False
            channel = guild.get_channel(channelId)

        if channel == None:
            channel = await category.create_text_channel(name)

        SqliteConnection.set_channel(
            guild.id, channel.id, textChannelType, name, isInsert=isInsert
        )

    return


async def create_management_channel(guild: Guild, members: Sequence[Member]):
    categoryType = ChannelData.get_channel_type("category")
    textChannelType = ChannelData.get_channel_type("text")
    categoryId = SqliteConnection.get_channel(guild.id, "管理用", categoryType)
    category = None
    isInsert = True
    if categoryId != None:
        isInsert = False
        category = guild.get_channel(categoryId)

    if category == None:
        category = await guild.create_category("管理用")
        SqliteConnection.set_channel(
            guild.id, category.id, categoryType, "管理用", isInsert=isInsert
        )

    # チャンネル名のリスト
    channel_list = ["コマンド", "ログ"]

    for name in channel_list:
        channelId = SqliteConnection.get_channel(guild.id, name, textChannelType)
        channel = None
        isInsert = True
        if channelId != None:
            isInsert = False
            channel = guild.get_channel(channelId)
        if channel == None:
            channel = await category.create_text_channel(name)
            SqliteConnection.set_channel(
                guild.id, channel.id, textChannelType, name, isInsert=isInsert
            )

    return
