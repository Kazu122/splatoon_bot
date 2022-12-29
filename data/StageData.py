# ステージ用のデータクラス
class StageData:
    # ステージリスト
    _stage_list: list[str] = [
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

    @classmethod
    def get_stage_list(cls):
        return cls._stage_list

    @classmethod
    def is_exist(cls, stage: str):
        return stage in cls._stage_list
