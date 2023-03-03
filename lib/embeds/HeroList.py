import disnake

class HeroList:
    def __init__(self, data):
        self.data = data
    
    async def ListEmbed(self):
        embed = disnake.Embed(title=f"{len(self.data)} Results")
        embed.color = disnake.Color.from_rgb(43, 45, 49)
        hero_names = [f"{i+1}. {hero['name']}" for i, hero in enumerate(iterable=self.data)]
        embed.description = "\n".join(hero_names)
        return embed
