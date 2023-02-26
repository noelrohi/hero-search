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
                return await inter.reply("Search with atleast 4 letter ;p ")
            gt_api = GT_API()
            response = await gt_api.find_heroes(page=1, params=params)
            data = response['data']
            pagination = response['meta']['pagination']
            if pagination['total'] > 1:
                embed = await HeroList(pagination=pagination, data=data).ListEmbed()
                # HeroList to iterate for Select Dropdown
                heroList = [{'label': f"{i+1}. {hero['attributes']['name']}", 'value': hero['id']} for i, hero in enumerate(iterable=data)]
                # Passing herolist, embed(For Back Button)
                view = HeroesView(heroList, embed)
                await inter.send(content = None, embed=embed, view=view)
                
            elif pagination['total'] == 1:
                data = await gt_api.getHero(data[0]['id'])
                hero_data = data['data']['attributes']
                hero =  Hero(hero_data)
                embed = await hero.hero_embed()
                view = HeroDetails(embed)
                await inter.send(content = None, embed=embed, view=view)
        except Exception as e:
            print(e)
    
def setup(bot):
    bot.add_cog(Nru(bot))