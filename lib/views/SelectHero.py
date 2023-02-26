import disnake
from disnake.ext import commands
from modules.gt import GT_API
from lib.embeds.Hero import Hero
import asyncio
        
class HeroDropdown(disnake.ui.StringSelect):
    def __init__(self, heroList, embed):
        self.heroList = heroList
        self.embed = embed
        # Define the options that will be presented inside the dropdown
        options = [disnake.SelectOption(label=f"{hero['label']}", value=f"{hero['value']}") for hero in self.heroList]

        super().__init__(
            placeholder="Choose a Hero",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, inter: disnake.MessageInteraction):
        # try:
            await inter.response.defer()
            data = await GT_API().getHero(self.values[0])
            hero_data = data['data']['attributes']
            hero =  Hero(hero_data)
            embed = await hero.hero_embed()
            view = HeroDetails(heroList = self.heroList, embed = self.embed, heroEmbed = embed)
            await inter.edit_original_message(embed=embed, view=view)
        # except Exception as e:
        #     print(e)

class HeroesView(disnake.ui.View):
    def __init__(self, heroList, embed):
        super().__init__(timeout=60)

        # Add the dropdown to our view object.
        self.dropdown = HeroDropdown(heroList, embed)
        self.add_item(self.dropdown)
        
class HeroDetails(disnake.ui.View):    
    def __init__(self, heroEmbed, heroList=None, embed = None):
        super().__init__(timeout=60)
        self.heroList = heroList
        self.embed = embed # Embed on-back btn
        self.heroEmbed = heroEmbed
        self.remove_item(self.stats)
        if heroList is None:
            self.remove_item(self.back)
        
    @disnake.ui.button(label="Back", style=disnake.ButtonStyle.grey)
    async def back(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        view = HeroesView(self.heroList, self.embed)
        await inter.response.edit_message(embed=self.embed, view=view)
        
    @disnake.ui.button(emoji="🔍", style=disnake.ButtonStyle.grey)
    async def zoom(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        embed = disnake.Embed()
        embed.title =self.heroEmbed.title
        embed.set_image(url=str(self.heroEmbed.thumbnail.url))
        embed.color = disnake.Color.from_rgb(43, 45, 49)
        self.remove_item(self.zoom)
        self.add_item(self.stats)
        await inter.response.edit_message(embed=embed,view=self)
    
    @disnake.ui.button(emoji="📊", style=disnake.ButtonStyle.grey)
    async def stats(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.remove_item(self.stats)
        self.add_item(self.zoom)
        await inter.response.edit_message(embed=self.heroEmbed,view=self)