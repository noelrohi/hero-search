import disnake
from lib.emojis.Ailments import Ailments

class Hero:
    def __init__(self, data):
        self.name = data['name']
        self.element = data['element']
        self.clas5 = data['class']
        self.equipment = data['equipment']
        self.rarity = "⭐⭐⭐" if data['rarity'] == "unique" else "⭐⭐"
        self.normal_attack = data['normal_attack']
        self.chain_skill = data['chain_skill']
        self.special_ability = data['special_ability'] 
        self.image_urls = data['image_urls']
        
    async def hero_embed(self, page:int = 0, zoom: bool = False):
        embeds = await self.getEmbeds(zoom)
        return embeds[page]
    
    async def getEmbeds(self, zoom):
        if zoom  is False:
            embeds = []
            urls = [self.image_urls['gl'], self.image_urls['jp'], self.image_urls['sc']]
            for url in urls:
                embed = disnake.Embed()
                embed.title = self.name
                descriptions = [f"**Element: ** {self.element}", f"**Class: ** {self.clas5}", f"**Weapon: ** {self.equipment}", f"**Rarity: ** {self.rarity}"]
                embed.description = "\n".join(descriptions)
                embed.add_field(name=self.normal_attack['title'], value=self.normal_attack['description'])
                embed.add_field(name=self.chain_skill['title'], value=f"{Ailments[self.chain_skill['Ailment']['from']]}»{Ailments[self.chain_skill['Ailment']['to']]}\n{self.chain_skill['description']}")
                embed.add_field(name=self.special_ability['title'], value=self.special_ability['description'])
                embed.set_thumbnail(url=url)
                embed.color = disnake.Color.from_rgb(43, 45, 49)
                embeds.append(embed)
            return embeds
        else:
            embeds = []
            urls = [self.image_urls['jp'], self.image_urls['gl'], self.image_urls['sc']]
            for url in urls:
                embed = disnake.Embed()
                embed.title = self.name
                embed.set_image(url=url)
                embed.color = disnake.Color.from_rgb(43, 45, 49)
                embeds.append(embed)
            return embeds