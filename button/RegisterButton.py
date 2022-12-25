import discord
from discord import Interaction
from discord import ButtonStyle


class WinButton(discord.ui.Button):
    def __init__(
        self, label: str = "win", style: ButtonStyle = ButtonStyle.success, row: int = 1
    ):
        super().__init__(label=label, style=style, row=row)

    async def callback(self, ctx: Interaction):
        await ctx.response.send_message("win")


class LoseButton(discord.ui.Button):
    def __init__(
        self,
        label: str = "lose",
        style: ButtonStyle = ButtonStyle.primary,
        row: int = 1,
    ):
        super().__init__(label=label, style=style, row=row)

    async def callback(self, ctx: Interaction):
        await ctx.response.send_message("lose")


class FinishButton(discord.ui.Button):
    def __init__(
        self, label: str = "fin", style: ButtonStyle = ButtonStyle.success, row: int = 1
    ):
        super().__init__(label=label, style=style, row=row)

    async def callback(self, ctx: Interaction):
        await ctx.response.send_message("fin")


class DeleteButton(discord.ui.Button):
    def __init__(
        self, label: str = "del", style: ButtonStyle = ButtonStyle.danger, row: int = 2
    ):
        super().__init__(label=label, style=style, row=row)

    async def callback(self, ctx: Interaction):
        await ctx.response.send_message("del")


class InitButton(discord.ui.Button):
    def __init__(
        self,
        label: str = "init",
        style: ButtonStyle = ButtonStyle.secondary,
        row: int = 2,
    ):
        super().__init__(label=label, style=style, row=row)

    async def callback(self, ctx: Interaction):
        await ctx.response.send_message("init")


class RegisterButton(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(WinButton())
        self.add_item(LoseButton())
        self.add_item(FinishButton())
        self.add_item(DeleteButton())
        self.add_item(InitButton())
