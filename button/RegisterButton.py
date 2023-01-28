import discord
from discord import Interaction
from discord import ButtonStyle
from data.ResultData import ResultData
from logic.create_embed import create_result_embed
from logic.create_stage_message import create_stage_message
from logic.utils import is_not_pined_message
from spreadsheet.PostGasScript import PostGasScript
from spreadsheet.connect_sheet import OperateSpreadSheet
import traceback


class RuleButton(discord.ui.Button):
    def __init__(
        self,
        rule: str = "ナワバリバトル",
        label: str = "ナワバリ",
        style: ButtonStyle = ButtonStyle.primary,
        row: int = 1,
    ):
        self.rule = rule
        super().__init__(label=label, style=style, row=row)

    async def callback(self, ctx: Interaction):
        await ctx.response.send_message(self.rule, delete_after=60)
        try:
            await create_stage_message(ctx, self.rule)
        except:
            traceback.print_exc()
            await ctx.followup.send("メッセージの作成に失敗しました")


class WinButton(discord.ui.Button):
    def __init__(
        self, label: str = "win", style: ButtonStyle = ButtonStyle.success, row: int = 3
    ):
        super().__init__(label=label, style=style, row=row)

    async def callback(self, ctx: Interaction):
        await ctx.response.send_message("win", delete_after=60)
        PostGasScript.post("addMatch")
        ResultData.add_result()
        message = ResultData.get_result_message()
        embed = create_result_embed()
        await message.edit(embed=embed)
        # await ctx.followup.send("win", delete_after=60)


class LoseButton(discord.ui.Button):
    def __init__(
        self,
        label: str = "lose",
        style: ButtonStyle = ButtonStyle.primary,
        row: int = 3,
    ):
        super().__init__(label=label, style=style, row=row)

    async def callback(self, ctx: Interaction):
        await ctx.response.send_message("lose", delete_after=60)
        PostGasScript.post("addMatch")
        ResultData.add_result()
        message = ResultData.get_result_message()
        embed = create_result_embed()
        await message.edit(embed=embed)


class FinishButton(discord.ui.Button):
    def __init__(
        self, label: str = "fin", style: ButtonStyle = ButtonStyle.success, row: int = 3
    ):
        super().__init__(label=label, style=style, row=row)

    async def callback(self, ctx: Interaction):
        await ctx.response.send_message("fin", delete_after=60)
        OperateSpreadSheet.set_result_data()
        ResultData.init_result()
        PostGasScript.post("registerResult")
        # 結果メッセージ(ピン止めされているメッセージ)以外を消去
        # TODO: スレッドも削除
        for thread in ctx.channel.threads:
            await thread.delete()
        await ctx.channel.purge(check=is_not_pined_message)
        message = ResultData.get_result_message()
        oldEmbed = message.embeds
        embed = create_result_embed()
        await message.edit(embed=embed)


class DeleteButton(discord.ui.Button):
    def __init__(
        self, label: str = "del", style: ButtonStyle = ButtonStyle.danger, row: int = 3
    ):
        super().__init__(label=label, style=style, row=row)

    # TODO 長さ1のときに動かないようにする
    async def callback(self, ctx: Interaction):
        await ctx.response.send_message("del", delete_after=60)
        if not (ResultData.delete_result()):
            return

        PostGasScript.post("deleteMatch")
        message = ResultData.get_result_message()
        embed = create_result_embed()
        await message.edit(embed=embed)


# TODO: シートも初期化
class InitButton(discord.ui.Button):
    def __init__(
        self,
        label: str = "init",
        style: ButtonStyle = ButtonStyle.secondary,
        row: int = 4,
    ):
        super().__init__(label=label, style=style, row=row)

    async def callback(self, ctx: Interaction):
        await ctx.response.send_message("init", delete_after=60)
        ResultData.init_result()
        message = ResultData.get_result_message()
        embed = create_result_embed()
        await message.edit(embed=embed)


class RegisterButton(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(RuleButton(rule="ナワバリバトル", label="ナワバリ", row=1))
        self.add_item(RuleButton(rule="ガチエリア", label="エリア", row=1))
        self.add_item(RuleButton(rule="ガチヤグラ", label="ヤグラ", row=1))
        self.add_item(RuleButton(rule="ガチホコ", label="ホコ", row=2))
        self.add_item(RuleButton(rule="ガチアサリ", label="アサリ", row=2))
        self.add_item(WinButton())
        self.add_item(LoseButton())
        self.add_item(FinishButton())
        self.add_item(DeleteButton())
        self.add_item(InitButton())
