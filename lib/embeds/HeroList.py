import disnake

class HeroList:
    def __init__(self, pagination, data):
        self.pagination = pagination
        self.data = data
    
    async def ListEmbed(self):
        embed = disnake.Embed(title=f"{self.pagination['total']} Results")
        embed.color = disnake.Color.from_rgb(43, 45, 49)
        hero_names = [f"{i+1}. {hero['attributes']['name']}" for i, hero in enumerate(iterable=self.data)]
        embed.description = "\n".join(hero_names)
        return embed
