import discord
import random

async def scan_message(bot: discord.Bot, message: discord.Message):
    words = message.content.split(' ')
    er_words = []
    for word in words:
        word = "".join(filter(lambda c: c.isalpha(), word))
        if len(word) < 2:
            continue
        if word[-2:] == 'er':
            er_words.append(word)
    if not er_words:
        return
    target = random.choice(er_words)
    await message.channel.send(f"{target}? I hardly know her!")