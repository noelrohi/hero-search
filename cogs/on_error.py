from disnake.ext import commands
import disnake
from datetime import timedelta, datetime

class OnError(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, inter, error):
        if isinstance(error, commands.MissingRequiredArgument):
            str = "Missing required argument!\nTry: `$lu earth or $lu fox`"
            embed = disnake.Embed(description=str)
            embed.colour = disnake.Color.red()
            await inter.reply(embed=embed)
        elif isinstance(error, commands.CommandOnCooldown):
            cooldown_time = error.retry_after
            cooldown_timestamp = int((datetime.now() + timedelta(seconds=cooldown_time)).timestamp())
            timestamp_str = f"Try again <t:{cooldown_timestamp}:R>"
            embed = disnake.Embed(description=timestamp_str)
            embed.colour = disnake.Color.red()
            await inter.reply(embed=embed)
def setup(bot):
    bot.add_cog(OnError(bot))