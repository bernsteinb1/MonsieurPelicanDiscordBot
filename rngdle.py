# RNGdle 🎲 865364

# 🟩 UNCOMMON • Top 45%

# 🟩 🍽️ Eighty-Six
# 🟩 🔗 2 Consecutive Numbers (Nearby)
# ⬜ 🧩 Mini Scramble
# +10 more

# 6,265 EP
import discord
import datetime
import daily_game

class RNGdle(daily_game.DailyGame):
    def __init__(self):
        super().__init__("rngdle")

async def try_parse_message(message: discord.Message):
        content = message.content
        if not content.startswith("RNGdle"):
            return
        lines = content.split('\n')
        try:
            score = int(lines[9][:-3].replace(",", ""))
        except Exception:
            await message.reply("Failed to parse RNGdle message")
            return
        author = message.author.id
        message_id = message.id
        date = message.created_at.date()
        result = game.insert_score(date, author, message_id, score)
        if not result:
            await message.reply("Result not stored. You have already submitted a result today!")
        else:
            await message.reply(f"Result stored.")
        
game = RNGdle()
        
