from discord import ui
import discord

# ダイアログ上でドロップダウンは使えないらしい
class RegisterWeaponDialog(ui.Modal):
    def __init__(
        self,
        rules: list[str],
        players: list[str],
        stages: list[str],
        weapons: list[str],
    ):
        super().__init__(
            "武器登録",
            timeout=None,
        )
        self.rule = ui.Select(label="rule", options=rules)
        self.player = ui.Select(label="player", options=players)
        self.stage = ui.Select(label="stage", options=stages)
        self.weapon = ui.Select(label="weapon", options=weapons)

    async def on_submit(self, interaction: discord.Interaction):
        bind = []
        if len(self.rule.values) == 0:
            await interaction.response.send_message("fail")
        if len(self.player.values) == 0:
            await interaction.response.send_message("fail")
        if len(self.stage.values) == 0:
            await interaction.response.send_message("fail")
        if len(self.weapon.values) == 0:
            await interaction.response.send_message("fail")

        bind.append(self.rule.values[0])
        bind.append(self.player.values[0])
        bind.append(self.stage.values[0])
        bind.append(self.weapon.values[0])
        await interaction.response.send_message("success")
