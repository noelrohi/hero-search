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
            hero_data = data['data']
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
        self.listEmbed = embed
        self.zoomEmbed = None # Embed on-back btn
        self.statEmbed = heroEmbed
        self.isZoomed = False
        self.image_gl = heroEmbed.thumbnail.url
        self.image_jp = heroEmbed.thumbnail.url.replace(".png","JP.png")
        self.image_sc = heroEmbed.thumbnail.url.replace(".png","SC.png")
        print(f"GL: {self.image_gl}, SC: {self.image_sc}, JP: {self.image_jp}")
        self.remove_item(self.stats)
        self.gl.disabled = True
        if heroList is None:
            self.remove_item(self.back)
        if self.zoomEmbed is None:
            embed = disnake.Embed()
            embed.title =self.statEmbed.title
            embed.set_image(url=str(self.statEmbed.thumbnail.url))
            embed.color = disnake.Color.from_rgb(43, 45, 49)
            self.zoomEmbed = embed
        
    @disnake.ui.button(label="Back", style=disnake.ButtonStyle.grey)
    async def back(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        view = HeroesView(self.heroList, self.listEmbed)
        await inter.response.edit_message(embed=self.listEmbed, view=view)
        
    @disnake.ui.button(emoji="🔍", style=disnake.ButtonStyle.grey)
    async def zoom(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.isZoomed = True
        self.remove_item(self.zoom)
        self.add_item(self.stats)
        await inter.response.edit_message(embed=self.zoomEmbed,view=self)
    
    def enableButtons(self):
        for child in self.children:
            child.disabled = False
            
    @disnake.ui.button(emoji="📊", style=disnake.ButtonStyle.grey)
    async def stats(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.remove_item(self.stats)
        self.add_item(self.zoom)
        self.isZoomed = False
        await inter.response.edit_message(embed=self.statEmbed,view=self)
        
    @disnake.ui.button(label="GL", style=disnake.ButtonStyle.grey)
    async def gl(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.enableButtons()
        self.gl.disabled = True
        if self.isZoomed:
            self.zoomEmbed.set_image(self.image_gl)
            await inter.response.edit_message(embed=self.zoomEmbed,view=self)
        else:
            self.statEmbed.set_thumbnail(self.image_gl)
            await inter.response.edit_message(embed=self.statEmbed,view=self)
    
    @disnake.ui.button(label="JP", style=disnake.ButtonStyle.grey)
    async def jp(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.enableButtons()
        self.jp.disabled = True
        # print(self.zoomEmbed.image.url)
        # print(self.image_jp)
        if self.isZoomed:
            self.zoomEmbed.set_image(self.image_jp)
            await inter.response.edit_message(embed=self.zoomEmbed,view=self)
            
        else:
            self.statEmbed.set_thumbnail(self.image_jp)
            await inter.response.edit_message(embed=self.statEmbed,view=self)
            
        
    @disnake.ui.button(label="SC", style=disnake.ButtonStyle.grey)
    async def sc(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.enableButtons()
        self.sc.disabled = True
        if self.isZoomed:
            self.zoomEmbed.set_image(self.image_sc)
            await inter.response.edit_message(embed=self.zoomEmbed,view=self)
        else:
            self.statEmbed.set_thumbnail(self.image_gl)
            await inter.response.edit_message(embed=self.statEmbed,view=self)