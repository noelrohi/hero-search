import disnake
from disnake.ext import commands
import asyncio
class OnStart(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):

        act = disnake.Activity(name="Okayge", type=disnake.ActivityType.listening)
        await self.bot.change_presence(status=disnake.Status.dnd, activity = act)
        print(f"Logged in as {self.bot.user} (ID: {self.bot.user.id})")

def setup(bot):
    bot.add_cog(OnStart(bot))