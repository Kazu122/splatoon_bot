import discord
from discord import Interaction
from data.StageData import StageData
from logic.utils import is_not_pined_message


class MapSelect(discord.ui.Select):
    def __init__(
        self,
        options: list[discord.SelectOption],
        placeholder="Map",
        row: int = 1,
    ):
        super().__init__(row=row, placeholder=placeholder, options=options)

    async def callback(self, ctx: Interaction):
        await ctx.response.send_message("search map", delete_after=60)
        await ctx.channel.purge(check=is_not_pined_message)
        if self.values == 0:
            return
        stage_name = self.values[0]
        fname = f"map.webp"
        file = discord.File(
            fp=f"./img/map/{stage_name}.webp", filename=fname, spoiler=False
        )
        embed = discord.Embed(title=stage_name, color=0x00FF00)
        embed.set_image(url=f"attachment://{fname}")
        await ctx.channel.send(file=file, embed=embed)


# map画像を選択するドロップダウン
class SearchView(discord.ui.View):
    def __init__(self):
        super().__init__()
        stage_list = StageData.get_stage_list()
        stage_options = [discord.SelectOption(label=stage) for stage in stage_list]
        self.add_item(MapSelect(placeholder="Map", options=stage_options))
