import discord
from discord import Interaction
from discord import ButtonStyle
from discord.ui import Button
from data.global_data import DataStore
from logic.create_embed import create_result_embed


class WinButton(Button):
    def __init__(
        self, stage: str, label: str = "win", style: ButtonStyle = ButtonStyle.success
    ):
        super().__init__(label=label, style=style)
        self.stage = stage

    async def callback(self, ctx: Interaction):
        await ctx.response.send_message("win", delete_after=60)
        DataStore.set_result(self.stage, "〇")
        message = DataStore.get_result_message()
        embed = create_result_embed()
        await message.edit(embed=embed)


class LoseButton(Button):
    def __init__(
        self, stage: str, label: str = "lose", style: ButtonStyle = ButtonStyle.primary
    ):
        super().__init__(label=label, style=style)
        self.stage = stage

    async def callback(self, ctx: Interaction):
        await ctx.response.send_message("lose", delete_after=60)
        DataStore.set_result(self.stage, "✕")
        message = DataStore.get_result_message()
        embed = create_result_embed()
        await message.edit(embed=embed)


class InitButton(Button):
    def __init__(
        self,
        stage: str,
        label: str = "init",
        style: ButtonStyle = ButtonStyle.secondary,
    ):
        super().__init__(label=label, style=style)
        self.stage = stage

    async def callback(self, ctx: Interaction):
        await ctx.response.send_message("init", delete_after=60)
        DataStore.set_result(self.stage, "ー")
        message = DataStore.get_result_message()
        embed = create_result_embed()
        await message.edit(embed=embed)


class StageButton(discord.ui.View):
    def __init__(self, stage: str):
        super().__init__()
        self.add_item(WinButton(stage=stage))
        self.add_item(LoseButton(stage=stage))
        self.add_item(InitButton(stage=stage))
