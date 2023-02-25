import disnake
from disnake.ext import commands
from modules.gt import GT_API
from lib.embeds.Hero import Hero

class HeroDropdown(disnake.ui.StringSelect):
    def __init__(self, heroList, embed, author):
        self.heroList = heroList
        self.embed = embed
        self.author = author
        # Define the options that will be presented inside the dropdown
        options = [disnake.SelectOption(label=f"{hero['label']}", value=f"{hero['value']}") for hero in self.heroList]

        super().__init__(
            placeholder="Choose a Hero",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, inter: disnake.MessageInteraction):
        if self.author.id != inter.author.id:
            return await inter.send("You are not allowed to interact!",ephemeral=True)
        data = await GT_API().getHero(self.values[0])
        hero_data = data['data']['attributes']
        hero =  Hero(hero_data)
        embed = await hero.hero_embed()
        view = BackButton(self.heroList, self.embed, self.author)
        await inter.response.edit_message(embed=embed, view=view)


class HeroesView(disnake.ui.View):
    def __init__(self, heroList, embed, author):
        super().__init__()

        # Add the dropdown to our view object.
        self.dropdown = HeroDropdown(heroList, embed, author)
        self.add_item(self.dropdown)
        
    async def on_timeout(self):
        self.dropdown.disabled = True
        
class BackButton(disnake.ui.View):
    def __init__(self, heroList, embed, author):
        super().__init__()
        self.heroList = heroList
        self.embed = embed
        self.author = author
        
    @disnake.ui.button(label="Back", style=disnake.ButtonStyle.grey)
    async def back(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if self.author.id != inter.author.id:
            return await inter.send("You are not allowed to interact!",ephemeral=True)
        view = HeroesView(self.heroList, self.embed, self.author)
        await inter.response.edit_message(embed = self.embed, view=view)