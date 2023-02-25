import disnake
from disnake.ext import commands
from modules.gt import GT_API
from lib.embeds.Hero import Hero
from lib.views.SelectHero import HeroesView

class Nru(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.command(aliases=['lu'])
    async def lookup(self, inter, params):
        msg = await inter.reply("Please wait.. ")
        gt_api = GT_API()
        response = await gt_api.find_heroes(page=1, params=params)
        data = response['data']
        pagination = response['meta']['pagination']
        if pagination['total'] > 1:
            embed = disnake.Embed(title=f"{pagination['total']} Results")
            embed.color = disnake.Color.from_rgb(43, 45, 49)
            hero_names = [f"{i+1}. {hero['attributes']['name']}" for i, hero in enumerate(iterable=data)]
            embed.description = "\n".join(hero_names)
            
            heroList = [{'label': f"{i+1}. {hero['attributes']['name']}", 'value': hero['id']} for i, hero in enumerate(iterable=data)]
            view = HeroesView(heroList, embed, inter.author)
            await msg.delete()
            await inter.reply(embed=embed, view=view, mention_author=False)
        elif pagination['total'] == 1:
            data = await gt_api.getHero(data[0]['id'])
            hero_data = data['data']['attributes']
            hero =  Hero(hero_data)
            embed = await hero.hero_embed()
            await msg.delete()
            await inter.reply(embed=embed, mention_author=False)
    
def setup(bot):
    bot.add_cog(Nru(bot))