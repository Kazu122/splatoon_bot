BEGIN TRANSACTION;

INSERT OR IGNORE INTO TBL_STAGE(name)
    VALUES("ゴンズイ地区"),
    ("スメーシーワールド"),
    ("キンメダイ美術館"),
    ("マテガイ放水路"),
    ("マヒマヒリゾート&スパ"),
    ("海女美術大学"),
    ("ナメロウ金属"),
    ("チョウザメ造船"),
    ("ヤガラ市場"),
    ("ザトウマーケット"),
    ("ユノハナ大渓谷"),
    ("マサバ海峡大橋"),
    ("ヒラメが丘団地"),
    ("クサヤ温泉");

INSERT OR IGNORE INTO TBL_RULE(rule)
    VALUES("ナワバリバトル"),
    ("ガチエリア"),
    ("ガチヤグラ"),
    ("ガチホコ"),
    ("ガチアサリ");

COMMIT TRANSACTION;