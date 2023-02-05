import discord

from data.ResultData import ResultData
from logic.create_embed import create_result_embed

# ダイアログ上でドロップダウンは使えないらしい
class OpenRegisterWeaponDialogButton(discord.ui.Button):
    def __init__(
        self,
        label: str = "open",
        style: discord.ButtonStyle = discord.ButtonStyle.secondary,
        row: int = 3,
    ):
        super().__init__(label=label, style=style, row=row)

    async def callback(self, ctx: discord.Interaction):
        await ctx.response.send_message("open", delete_after=60)
        ResultData.init_result()
        message = ResultData.get_result_message()
        embed = create_result_embed()
        await message.edit(embed=embed)


class OpenSearchWeaponDialogButton(discord.ui.Button):
    def __init__(
        self,
        label: str = "search",
        style: discord.ButtonStyle = discord.ButtonStyle.secondary,
        row: int = 3,
    ):
        super().__init__(label=label, style=style, row=row)

    async def callback(self, ctx: discord.Interaction):
        await ctx.response.send_message("search", delete_after=60)
        ResultData.init_result()
        message = ResultData.get_result_message()
        embed = create_result_embed()
        await message.edit(embed=embed)


class WeaponButton(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(OpenRegisterWeaponDialogButton())
        self.add_item(OpenSearchWeaponDialogButton())
