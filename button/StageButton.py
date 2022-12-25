import discord
from discord import Interaction
from discord import ButtonStyle
from discord.ui import Button
from data.global_data import stage_list


class WinButton(Button):
    def __init__(
        self, stage: str, label: str = "win", style: ButtonStyle = ButtonStyle.success
    ):
        super().__init__(label=label, style=style)
        self.stage = stage

    async def callback(self, ctx: Interaction):
        stage_list[self.stage] = "〇"
        await ctx.response.send_message("win")


class LoseButton(Button):
    def __init__(self, label: str = "lose", style: ButtonStyle = ButtonStyle.primary):
        super().__init__(label=label, style=style)

    async def callback(self, ctx: Interaction):
        await ctx.response.send_message("lose")


class InitButton(Button):
    def __init__(self, label: str = "init", style: ButtonStyle = ButtonStyle.secondary):
        super().__init__(label=label, style=style)

    async def callback(self, ctx: Interaction):
        await ctx.response.send_message("init")


class StageButton(discord.ui.View):
    def __init__(self, stage: str):
        super().__init__()
        self.add_item(WinButton(stage=stage))
        self.add_item(LoseButton(stage=stage))
        self.add_item(InitButton(stage=stage))
