import os
import asyncio
import cv2 as cv
import image_to_ascii as converter

from PIL import Image
from discord.ext import commands

os.path.join(os.getcwd())

class ASCII(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "say")
    async def helper_say(self, ctx, *, text):
        ctx.send(text)

    @commands.command(name = "ascii-video", aliases = ["ascii-v", "av"])
    async def show_ascii_video(self, ctx, filename, type = 1):
        # Chequear si el primer comando se envió correctamente
        if (not ctx.author.bot) and (type != 1):
            return await ctx.send("Comando invalido.")

        # Chequear si el primer mensaje lo recibió el HelperBot
        if (self.bot.user.name == "HelperBot") and (type == 1):
            return

        # Preparar capturadora y variables
        cap = cv.VideoCapture(f'videos/{filename}.mp4')
        index = 0

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                if type == 1:
                    await ctx.send("End of video! Thanks for watching! ^-^")
                elif type == 2:
                    await ctx.send("^-^")
                break

            out = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)
            pilimage = Image.fromarray(out)

            if type == 1:
                if index == 0:
                    # await ctx.send(ascii_image(pilimage))
                    await ctx.send(f"=av {filename} 2")
                    await asyncio.sleep(0.5)

                if index % 2 != 0:
                    # await ctx.send(f"{index}")
                    await ctx.send(content = "```\n" + converter.ascii_image(pilimage) + "\n```")
                    await asyncio.sleep(1)

            if type == 2:
                if index % 2 == 0:
                    # await ctx.send(f"{index}")
                    await ctx.send(content = "```\n" + converter.ascii_image(pilimage) + "\n```")
                    await asyncio.sleep(1)

            index += 1

        cap.release()

def setup(bot):
    bot.add_cog(ASCII(bot))