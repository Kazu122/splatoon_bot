import discord


def is_not_pined_message(message: discord.Message):
    return not (message.pinned)
