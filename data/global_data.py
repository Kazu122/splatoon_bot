import discord
from typing import Optional

# ステージリスト
stage_list: list[str] = [
    "ゴンズイ地区",
    "スメーシーワールド",
    "キンメダイ美術館",
    "マテガイ放水路",
    "マヒマヒリゾート&スパ",
    "海女美術大学",
    "ナメロウ金属",
    "チョウザメ造船",
    "ヤガラ市場",
    "ザトウマーケット",
    "ユノハナ大渓谷",
    "マサバ海峡大橋",
    "ヒラメが丘団地",
    "クサヤ温泉",
]

# ないとは思うが、複数サーバーに対応する場合はサーバーIDをキーとする辞書にする必要があるかも
result: dict = dict(zip(stage_list, [["ー"] for _ in stage_list]))

# リザルトのembedのメッセージオブジェクト
# 編集時にアクセスしやすいように保持しておく
class resultMessage:
    _result_message: Optional[discord.Message] = None

    @classmethod
    def get_result_message(cls):
        return cls._result_message

    @classmethod
    def set_result_message(cls, message):
        cls._result_message = message
