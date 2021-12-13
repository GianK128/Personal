import discord
import json, random, requests
from discord.ext import commands

class NSFW(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "rule34", aliases = ["r34"])
    async def search_r34(self, ctx, character: str, *, series: str = None):
        await ctx.message.reply("Ahí te busco.")

        if series is None:
            formatted_tags = f'{character})'
        else:
            formatted_tags = f'{character}_({series.strip().replace(" ", "_")})'

        try:
            payload = {
                "page" : "dapi",
                "s" : "post",
                "q" : "index",
                "json" : "1",
                "tags" : formatted_tags
            }
            response = requests.get("http://rule34.xxx/index.php", params = payload, headers = {"User-Agent" : "Discord-HentaiBot"})
            data = response.json()
        except json.JSONDecodeError:
            return await ctx.send(f"No encontré nada")
        
        count = len(data)

        if count == 0:
            await ctx.send(f"No pude encontrar resultados de {character}, de {series}")
            return
        
        image_count = count if count < 1000 else 1000

        index = random.randint(0, image_count)
        image = data[index]
        url = f"http://img.rule34.xxx/images/{image['directory']}/{image['image']}"

        em = discord.Embed(title = f"Acá esta tu porno de {character.capitalize()}", description = "Que lo disfrutes.", color = ctx.author.color)
        em.set_image(url = url)

        await ctx.message.reply(embed = em)

def setup(bot):
    bot.add_cog(NSFW(bot))