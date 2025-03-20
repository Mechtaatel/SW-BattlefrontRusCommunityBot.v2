from discord.ext import commands
from datetime import datetime
from os import path
# import logging #модуль logging используется для логирования 

# logging.basicConfig(level=logging.INFO) #Параметр level=logging.INFO устанавливает уровень логирования.
#     #В данном случае это INFO, что означает, что будут записываться сообщения уровня INFO и выше 
#     #(например, WARNING, ERROR, CRITICAL).
# logger = logging.getLogger(__name__) # Создает объект logger для текущего модуля (файла)
#     # __name__ — это специальная переменная, которая содержит имя текущего модуля. 
#     #Например, если этот код находится в файле say.py, то __name__ будет равно "commands.moderator_commands.say"


class Say:
    def __init__(self, bot):
        self.bot = bot
        self.setup()

    def setup(self):
        @self.bot.slash_command(name='say', description='Отправить сообщение от имени бота')
        @commands.has_permissions(administrator=True)
        async def say(ctx, message: str):
            await ctx.defer()
            log_file = path.join('logs', 'message_history.txt')
            with open(log_file, 'a', encoding='utf-8') as file:
                file.write(f'[{datetime.now()}] {ctx.author} использовал команду /say\n{message}\n')
            await ctx.respond(message)
            