import discord
from data.StageData import StageData
from typing import Optional

# 結果記録用のデータ格納用クラス
class ResultData:
    # リザルトのembedのメッセージオブジェクト
    # 編集時にアクセスしやすいように保持しておく
    _result_message: Optional[discord.Message] = None
    _result: dict[str, list[str]] = dict(
        zip(StageData.get_stage_list(), [["ー"] for _ in StageData.get_stage_list()])
    )

    @classmethod
    def get_result_message(cls):
        return cls._result_message

    @classmethod
    def set_result_message(cls, message):
        cls._result_message = message

    @classmethod
    def get_result(cls):
        return cls._result

    @classmethod
    def set_result(cls, key, value):
        cls._result[key][-1] = value

    @classmethod
    def add_result(cls):
        for array in cls._result.values():
            array.append("ー")

    @classmethod
    def delete_result(cls):
        for array in cls._result.values():
            del array[-1]

    @classmethod
    def init_result(cls):
        for key in cls._result.keys():
            cls._result[key] = ["ー"]
