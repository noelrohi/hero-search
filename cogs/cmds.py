import disnake
from disnake.ext import commands
from modules.gt import GT_API
from lib.embeds.Hero import Hero
from lib.views.SelectHero import HeroesView, HeroDetails
from lib.embeds.HeroList import HeroList

class Nru(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    # @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.command(aliases=['lu'])
    async def lookup(self, inter, params):
        try:
            if len(params) < 4:
                return await inter.reply("`Search with atleast 4 letter ;p `")
            gt_api = GT_API()
            response = await gt_api.find_heroes(params=params)
            if response:
                heroList = response['data']
                heroCount = len(heroList)
                if heroCount > 1:
                    quotient, remainder = divmod(len(heroList), 10)
                    sublists = [heroList[i:i+10] for i in range(0, 10*quotient, 10)]
                    if remainder:
                        sublists.append(heroList[-remainder:])
                # for data in sublists:
                    data = sublists[0]
                    embed = await HeroList(data).ListEmbed()
                    # HeroList to iterate for Select Dropdown
                    heroList = [{'label': f"{i+1}. {hero['name']}", 'value': hero['_id']} for i, hero in enumerate(iterable=data)]
                    # Passing herolist, embed(For Back Button)
                    view = HeroesView(heroList, embed)
                    await inter.send(content = None, embed=embed, view=view)
                    
                elif heroCount == 1:
                    data = await gt_api.getHero(heroList[0]['_id'])
                    hero_data = data['data']
                    hero =  Hero(hero_data)
                    embed = await hero.hero_embed()
                    view = HeroDetails(embed)
                    await inter.send(content = None, embed=embed, view=view)
                else:
                    await inter.send(content = f"Looked up {params} but I have found nothing. ")
        except Exception as e:
            print(e)
    
def setup(bot):
    bot.add_cog(Nru(bot))