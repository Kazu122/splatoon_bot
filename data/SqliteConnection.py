import sqlite3
from typing import Union

# sqlite3のdbとやりとりをするクラス
class SqliteConnection:
    conn = None

    @classmethod
    def set_connection(cls):
        cls.conn = sqlite3.connect("./db/splabot.db")

    @classmethod
    def get_connection(cls):
        return cls.conn

    @classmethod
    def close(cls):
        if cls.conn != None:
            cls.conn.close()

    @classmethod
    def get_stage_data(cls) -> list[list[any]]:
        conn = cls.get_connection()
        cur = conn.cursor()
        try:
            # ステージデータの取得
            sql = f"""
                SELECT id, name FROM TBL_STAGE;
            """
            cur.execute(sql)
            return cur.fetchall()
        except Exception:
            raise

    @classmethod
    def get_rule_data(cls) -> list[list[any]]:
        conn = cls.get_connection()
        cur = conn.cursor()
        try:
            # ルールデータの取得
            sql = f"""
                SELECT id, rule FROM TBL_RULE;
            """
            cur.execute(sql)
            return cur.fetchall()
        except Exception:
            raise

    @classmethod
    def get_rule_id(cls, name: str) -> list[list[any]]:
        conn = cls.get_connection()
        cur = conn.cursor()
        try:
            # ルールデータの取得
            sql = f"""
                SELECT id FROM TBL_RULE
                    WHERE rule = ?;
            """
            cur.execute(sql, (name,))
            return cur.fetchone()[0]
        except Exception:
            raise

    @classmethod
    def get_member_data(cls, guildId: int) -> list[list[any]]:
        conn = cls.get_connection()
        cur = conn.cursor()
        try:
            # ルールデータの取得
            sql = f"""
                SELECT id, name FROM TBL_PLAYER
                    WHERE guildId = ?;
            """
            cur.execute(sql, (str(guildId),))
            return cur.fetchall()
        except Exception:
            raise

    @classmethod
    def register_formation(cls, rule: str, stage: str, member: str, weapon: str):
        conn = cls.get_connection()
        cur = conn.cursor()
        try:
            # playerデータの取得
            sql = f"""
                SELECT id, guildId, name FROM TBL_PLAYER
                    WHERE name = ?;
            """
            cur.execute(sql, (member,))
            playerId = cur.fetchone()[0]

            # 武器データの取得
            sql = f"""
                SELECT * FROM TBL_WEAPON
                    WHERE name = ?;
            """
            cur.execute(sql, (weapon,))
            weaponId = cur.fetchone()[0]

            # ステージデータの取得
            sql = f"""
                SELECT * FROM TBL_STAGE
                    WHERE name = ?;
            """
            cur.execute(sql, (stage,))
            stageId = cur.fetchone()[0]

            # ルールデータの取得
            sql = f"""
                SELECT * FROM TBL_RULE
                    WHERE rule = ?;
            """
            cur.execute(sql, (rule,))
            ruleId = cur.fetchone()[0]

            sql = f"""
                SELECT * FROM TBL_FORMATION
                    WHERE playerId = ? AND ruleId = ? AND stageId = ?;
            """
            cur.execute(sql, (playerId, ruleId, stageId))
            formation = cur.fetchone()
            if formation == None:
                sql = f"""
                    INSERT INTO TBL_FORMATION(playerId, ruleId, stageId, weaponId)
                        VALUES(?,?,?,?)
                """
                cur.execute(sql, (playerId, ruleId, stageId, weaponId))

            else:
                sql = f"""
                    UPDATE TBL_FORMATION
                        SET weaponId = ?
                        WHERE id = ?
                """
                cur.execute(sql, (weaponId, formation[0]))
            conn.commit()
        except:
            raise Exception()

    @classmethod
    def get_formation_weapon_data(cls, rule: int, stage: int, member: int):
        conn = cls.get_connection()
        cur = conn.cursor()
        try:
            # playerデータの取得
            sql = f"""
                SELECT id, guildId, name FROM TBL_PLAYER
                    WHERE name = ?;
            """
            cur.execute(sql, (member,))
            playerId = cur.fetchone()[0]

            # ステージデータの取得
            sql = f"""
                SELECT * FROM TBL_STAGE
                    WHERE name = ?;
            """
            cur.execute(sql, (stage,))
            stageId = cur.fetchone()[0]

            # ルールデータの取得
            sql = f"""
                SELECT * FROM TBL_RULE
                    WHERE rule = ?;
            """
            cur.execute(sql, (rule,))
            ruleId = cur.fetchone()[0]

            sql = f"""
                SELECT weaponId FROM TBL_FORMATION
                    WHERE playerId = ? AND ruleId = ? AND stageId = ?;
            """
            cur.execute(sql, (playerId, ruleId, stageId))
            formation = cur.fetchone()

            # Noneの場合データベースに未登録
            if formation == None:
                return "未設定"

            # 武器idの取得
            id = formation[0]

            # 武器名の取得
            sql = f"""
                SELECT weapon, sub, special FROM VIEW_WEAPON
                    WHERE id = ?;
            """
            cur.execute(sql, (id,))
            weaponData = cur.fetchone()
            return weaponData
        except:
            raise Exception()

    # idからメンバーの使用武器を検索する
    @classmethod
    def get_formation_weapon_data_using_id(
        cls, ruleId: int, stageId: int, playerId: int
    ):
        conn = cls.get_connection()
        cur = conn.cursor()
        try:
            sql = f"""
                SELECT weaponId FROM TBL_FORMATION
                    WHERE playerId = ? AND ruleId = ? AND stageId = ?;
            """
            cur.execute(sql, (str(playerId), str(ruleId), str(stageId)))
            formation = cur.fetchone()

            # Noneの場合データベースに未登録
            if formation == None:
                return ["未設定", "未設定", "未設定"]

            # 武器idの取得
            id = formation[0]

            # 武器名の取得
            sql = f"""
                SELECT weapon, sub, special FROM VIEW_WEAPON
                    WHERE id = ?;
            """
            cur.execute(sql, (id,))
            weaponData = cur.fetchone()
            return weaponData
        except:
            raise Exception()

    # channelのidを取得する
    # typeは現状名称被りがないので使用しない
    @classmethod
    def get_channel(cls, guildId: int, name: str, type: int) -> Union[int, None]:
        conn = cls.get_connection()
        cur = conn.cursor()
        try:
            sql = f"""
                SELECT channelId FROM TBL_CHANNEL
                    WHERE guildId = ? AND name = ?;
            """
            cur.execute(sql, (str(guildId), name))
            channel = cur.fetchone()

            # Noneの場合データベースに未登録
            if channel == None:
                return None

            return int(channel[0])
        except:
            raise Exception()

    @classmethod
    def set_channel(
        cls, guildId: int, channelId: int, channelType: int, name: str, isInsert=True
    ):
        conn = cls.get_connection()
        cur = conn.cursor()
        try:
            if isInsert:
                # 存在しない場合は追加
                sql = f"""
                        INSERT OR IGNORE INTO TBL_CHANNEL(guildId, channelId, channelType, name)
                        VALUES(?, ?, ?, ?);
                    """
                cur.execute(sql, (str(guildId), str(channelId), channelType, name))
            else:
                # 存在する場合は更新
                sql = f"""
                        UPDATE TBL_CHANNEL
                            SET channelId = ?
                            WHERE guildId = ? AND channelType = ? AND name = ?;
                    """
                cur.execute(sql, (str(channelId), str(guildId), channelType, name))
            conn.commit()
            return
        except:
            raise Exception()
