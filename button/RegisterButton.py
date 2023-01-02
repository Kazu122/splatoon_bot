import discord
from discord import Interaction
from discord import ButtonStyle
from data.ResultData import ResultData
from logic.create_embed import create_result_embed
from spreadsheet.PostGasScript import PostGasScript
from spreadsheet.connect_sheet import OperateSpreadSheet


class WinButton(discord.ui.Button):
    def __init__(
        self, label: str = "win", style: ButtonStyle = ButtonStyle.success, row: int = 1
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
        row: int = 1,
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
        self, label: str = "fin", style: ButtonStyle = ButtonStyle.success, row: int = 1
    ):
        super().__init__(label=label, style=style, row=row)

    async def callback(self, ctx: Interaction):
        await ctx.response.send_message("fin", delete_after=60)
        OperateSpreadSheet.set_result_data()
        ResultData.init_result()
        PostGasScript.post("registerResult")
        message = ResultData.get_result_message()
        embed = create_result_embed()
        await message.edit(embed=embed)


class DeleteButton(discord.ui.Button):
    def __init__(
        self, label: str = "del", style: ButtonStyle = ButtonStyle.danger, row: int = 2
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


class InitButton(discord.ui.Button):
    def __init__(
        self,
        label: str = "init",
        style: ButtonStyle = ButtonStyle.secondary,
        row: int = 2,
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
        self.add_item(WinButton())
        self.add_item(LoseButton())
        self.add_item(FinishButton())
        self.add_item(DeleteButton())
        self.add_item(InitButton())
