import asyncio
from discord.ext import commands
from discord.flags import Intents
from credentials import token, helper_token

loop = asyncio.get_event_loop()

bot = commands.Bot(command_prefix = "=", intents = Intents.all())
helper_bot = commands.Bot(command_prefix = "=", intents = Intents.all())

@bot.event
async def on_ready():
    print(f"Logueado como:\n{bot.user.name}\n{bot.user.id}")

@helper_bot.event
async def on_ready():
    print(f"Logueado como:\n{helper_bot.user.name}\n{helper_bot.user.id}")

@helper_bot.event
async def on_message(message):
    ctx = await helper_bot.get_context(message)
    await bot.invoke(ctx)

bot.load_extension('nsfw_cog')

bot.load_extension('ascii_video_cog')
helper_bot.load_extension('ascii_video_cog')

loop.create_task(bot.start(token))
loop.create_task(helper_bot.start(helper_token))

try:
    loop.run_forever()
finally:
    loop.stop()