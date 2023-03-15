import disnake
from disnake.ext import commands
from modules.gt import GT_API
from lib.embeds.Hero import Hero
from lib.views.SelectHero import HeroesView, HeroDetails
from lib.embeds.HeroList import HeroList

class Slash(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command()
    async def lookup(self, inter: disnake.ApplicationCommandInteraction, params: str):
        """
        Lookup heroes
        Parameters
        ----------
        params : Search keywords
        """
        try:
            response = await self.api.find_heroes(params=params)
                
            heroList = response['data']
            print(len(heroList))
            heroCount = len(heroList)
            if heroCount == 0:
                return await inter.send(content = f"Looked up {params} but I have found nothing. ")
            elif heroCount > 1:
                quotient, remainder = divmod(len(heroList), 10)
                sublists = [heroList[i:i+10] for i in range(0, 10*quotient, 10)]
                if remainder:
                    sublists.append(heroList[-remainder:])
                data = sublists[0]
                embed = await HeroList(data).ListEmbed()
                heroList = [{'label': f"{i+1}. {hero['name']}", 'value': hero['_id']} for i, hero in enumerate(iterable=data)]
                view = HeroesView(heroList, embed)
                await inter.send(content = None, embed=embed, view=view)
                
            elif heroCount == 1:
                data = await self.api.getHero(heroList[0]['_id'])
                hero_data = data['data']
                hero =  Hero(hero_data)
                embed = await hero.hero_embed()
                view = HeroDetails(embed)
                await inter.send(content = None, embed=embed, view=view)
        except Exception as e:
            print(e)
    
    @lookup.autocomplete("params")
    async def lookup_autocomp(self, inter: disnake.ApplicationCommandInteraction, string: str):
        gt_api = GT_API()
        
        findData = await gt_api.find_heroes(params=string)
        data = findData['data']
        string = string.lower()
        if not string:
            string = "a"
        return [word['name'] for word in data[:25] if string in word['name'].lower()]
        ...
        
def setup(bot):
    bot.add_cog(Slash(bot))