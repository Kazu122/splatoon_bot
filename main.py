from discord.ext import tasks
import discord
import os
import json
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
from discord import Interaction
from logic.create_channel import *
from data import SqliteConnection

load_dotenv()

TOKEN = os.environ.get("TOKEN")


class MyClient(commands.Bot):
    def __init__(self, *, intents: discord.Intents):
        super().__init__("/", intents=intents)
        # self.tree = app_commands.CommandTree(self)
        SqliteConnection.set_connection()

    async def setup_hook(self):
        # self.tree.copy_global_to()
        await self.tree.sync()

    async def close(self) -> None:
        await super().close()
        SqliteConnection.close()
        return


intents = discord.Intents.all()  # Intentsオブジェクトを生成
client = MyClient(intents=intents)

# サーバーの初期化を行う
async def init(guild: Guild):
    members = guild.members

    await create_main_channel(guild, members)
    await create_data_channel(guild, members)
    await create_archive_channel(guild, members)
    await create_document_channel(guild, members)
    await create_management_channel(guild, members)


# TODO: チャンネルが存在する場合に取得してresult_messageをセットする
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    # TODO 起動時も初期化を行う
    guilds = client.guilds
    for guild in guilds:
        await init(guild)

    print("initialized complete")


# サーバーIDをデータベースへ登録する
@client.event
async def on_guild_join(guild: Guild):
    cur = None
    try:
        cur = SqliteConnection.get_connection().cursor()
        sql = (
            "PRAGMA foreign_keys=true;" "INSERT INTO TBL_GUILD(id, name) values(?, ?);"
        )
        cur.execute(sql, (guild.id, guild.name))
    except Exception as e:
        print(e)
    finally:
        if cur != None:
            cur.close()


# サーバーの更新があったときにDBも更新
@client.event
async def on_guild_update(before: Guild, after: Guild):
    cur = None
    try:
        cur = SqliteConnection.get_connection().cursor()
        sql = (
            "PRAGMA foreign_keys=true;"
            "UPDATE INTO TBL_GUILD SET name = ? WHERE id = ?;"
        )
        cur.execute(sql, after.name, before.id)
    except Exception as e:
        print(e)
    finally:
        if cur != None:
            cur.close()


# サーバーからクライアントが削除されたときにDBから削除
@client.event
async def on_guild_remove(guild: Guild):
    cur = None
    try:
        cur = SqliteConnection.get_connection().cursor()
        sql = "PRAGMA foreign_keys=true;" "DELETE FROM TBL_GUILD WHERE id = ?;"
        cur.execute(sql, (guild.id,))
    except Exception as e:
        print(e)
    finally:
        if cur != None:
            cur.close()


# testコマンド: テスト用
# @client.tree.command(name="test", description="test")
# async def test(ctx: Interaction):
#     await ctx.response.send_message(f"hello World", delete_after=30)


# setupコマンド: サーバーの初期設定を行う
@client.tree.command(name="setup", description="初期設定を行います")
async def setup(ctx: Interaction):
    await ctx.response.send_message(f"setup中", delete_after=120)
    await init(ctx.guild)
    await ctx.followup.send(f"setup完了")


# clearコマンド: チャンネルを全消去する
@client.tree.command(name="clear", description="チャンネルをすべて削除します")
async def clear(ctx: Interaction):
    await ctx.response.send_message(f"clear", delete_after=30)
    channels = await ctx.guild.fetch_channels()
    for channel in channels:
        await channel.delete()

    await ctx.guild.create_text_channel("command")
    await ctx.guild.create_voice_channel("test")


# memberコマンド: メンバーを登録する
@client.tree.command(name="member", description="チームメンバーをbotへ登録します")
async def register_member(
    ctx: Interaction, member1: str, member2: str, member3: str, member4: str
):
    await ctx.response.send_message(f"register member", delete_after=30)
    members = [member1, member2, member3, member4]
    conn = SqliteConnection.get_connection()
    cur = conn.cursor()
    try:
        for member in members:
            sql = f"""
                SELECT * FROM TBL_PLAYER
                WHERE guildId = ? AND name = ?
            """
            cur.execute(sql, (ctx.guild.id, member))
            player = cur.fetchone()
            if player == None:
                sql = f"""
                    INSERT INTO TBL_PLAYER(guildId, name)
                    VALUES(?,?)
                """
                cur.execute(sql, (ctx.guild.id, member))

            else:
                sql = f"""
                    UPDATE TBL_PLAYER
                    SET name = ?, guildId = ?
                    WHERE id = ?
                """
                cur.execute(sql, (member, ctx.guild.id, player[0]))
        conn.commit()
    except:
        pass


# weaponコマンド:
@client.tree.command(name="weapon", description="武器編成をbotへ登録します")
@discord.app_commands.choices(rule=[], stage=[], member=[], weapon=[])
async def edit_weapon(
    ctx: Interaction, rule: str, stage: str, member: str, weapon: str
):
    await ctx.response.send_message(f"edit weapon", delete_after=30)
    conn = SqliteConnection.get_connection()
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
            WHERE playerId = ? AND ruleId = ? AND stageId = ? AND weaponId = ?;
        """
        cur.execute(sql, (playerId, ruleId, stageId, weaponId))
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
            cur.execute(sql, (formation[4], formation[0]))
        conn.commit()
    except:
        await ctx.followup.send(f"武器変更に失敗しました")


# @client.listen("on_message")
# async def on_message(message: discord.Message):
#     if message.author == client.user:
#         return

#     await message.channel.send("Hello!")


client.run(TOKEN)
