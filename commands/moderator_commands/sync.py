from discord.ext import commands

class Sync:
    def __init__(self, bot):
        self.bot = bot
        self.setup()

    def setup(self):
        @self.bot.slash_command(name='sync', description='Синхронизировать команды')
        @commands.has_permissions(administrator=True)
        async def sync(ctx):
              # Синхронизация команд
            await ctx.respond("Команды синхронизированы!")