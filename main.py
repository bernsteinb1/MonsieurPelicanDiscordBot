import discord
import asyncio
import er
import dotenv
import os
import rngdle
import datetime

permissions_integer = 7389235682728000
dotenv.load_dotenv()
token = os.getenv("DISCORD_TOKEN")

class MonsieurPelican(discord.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        
    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        if message.content == 'Ping':
            await message.channel.send('Pong')
        await er.scan_message(self, message)
        await rngdle.try_parse_message(message)

# set up before initializing bot
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# make bot
bot = MonsieurPelican()

@bot.command(description="Index older results into database")
async def index_old_results(ctx: discord.ApplicationContext, scan_days: int = 10):
    await ctx.defer(ephemeral=True)
    
    if ctx.author.id != int(os.getenv("ADMIN_ID")):
        await ctx.respond("You do not have permission for this command.")
        return
    
    start_day = datetime.datetime.now(datetime.UTC) - datetime.timedelta(scan_days)

    channels = ctx.guild.channels
    
    for channel in channels:
        if channel.type != discord.ChannelType.text:
            continue
        async for message in channel.history(after=start_day, limit=None):
            await rngdle.try_parse_message(message)
    
    await ctx.respond("Done.")
    
@bot.slash_command(description="Compare your game results against anothers")
async def get_results(ctx: discord.ApplicationContext, user: discord.User, comp_user: discord.User):
    results = rngdle.game.get_record(user.id, comp_user.id)
    await ctx.respond(f"Here is {user.mention}'s record against {comp_user.mention}\n\nTotal games: {results[0]}\nWins: {results[1]}\nLosses: {results[2]}\nTies: {results[3]}")

permissions = discord.Permissions(permissions_integer)
url = discord.utils.oauth_url(1569012390421331988, permissions=permissions)
print(f"Invite the bot using {url}")

bot.run(token)
    
