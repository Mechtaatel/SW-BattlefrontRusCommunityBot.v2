import logging
logging.basicConfig(
    filename='app.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
import os
import json
from dotenv import load_dotenv
import re
import yt_dlp as youtube_dl
import asyncio
import discord
from datetime import datetime, timedelta
intents = discord.Intents.all()
intents.members = True  # Включаем intent для работы с участниками сервера
intents.presences = True  # Включаем intent для отслеживания активности
bot = discord.Bot(intents=intents)

@bot.event
async def on_presence_update(before, after):
    if before.activity != after.activity: # Проверяем, изменилась ли активность
        if after.activity and after.activity.type == discord.ActivityType.playing:
            if after.activity.name == "STAR WARS™ Battlefront™ II":
                with open('logs/game_activity.txt', 'a', encoding='utf-8') as file:
                    file.write(
                        f'[{datetime.now()}] {after.name} начал играть в {after.activity.name}.\n'
                    )
        else:
            return
    else:
        return
@bot.event
async def on_member_join(member):
    guild = bot.get_guild(1071600435607113819)
    if member.guild == guild:
        with open('commands/clan_commands/clan_members.json', 'r',  encoding='utf-8') as f:  # Загружаем данные из JSON файла
            clan_data = json.load(f)
        if str(member.id) not in clan_data: # Добавляем данные для пользователя которого еще нет в системе
            clan_data[str(member.id)] = { 
                "main_server": True,  # Есть ли на сервере
                "clan": False,  # Состояние в клане
                "ea_name": False}
            member.add_roles(guild.get_role(1165749431455461437))
        elif clan_data["clan"] == False:
            member.add_roles(guild.get_role(1165749431455461437))
        else:
            clan_name = clan_data['clan']
            member.add_roles(guild.get_role(clan_data['clan'][clan_name]))
    if clan_data:
        with open('commands/clan_commands/clan_members.json', 'w', encoding='utf-8') as f:
            json.dump(clan_data, f, indent=4, ensure_ascii=False)
@bot.event
async def on_member_remove(member):
    with open('commands/clan_commands/clan_members.json', 'r',  encoding='utf-8') as f:  # Загружаем данные из JSON файла
        clan_data = json.load(f)
    clan_data[member.id]["main_server"] = False
    with open('commands/clan_commands/clan_members.json', 'w', encoding='utf-8') as f:
        json.dump(clan_data, f, indent=4, ensure_ascii=False)
# ROLES_TO_CHECK = {"1071603880774877184": "Джедаи", "1172856253513474048": "Джедаи", "1071604138959454238": "Джедаи", "1071604404534390804": "Джедаи", "1071604570821759016": "Джедаи",
    #                   "1071604746609246238": "Джедаи", "1071604948476895263": "Джедаи", "1071605080953987262": "Ситхи", "1211985928759935056": "Ситхи", "1071605535964676128": "Ситхи",
    #                   "1071605371619266590": "Ситхи", "1071606012534079498": "Ситхи", "1071606225189470339": "Ситхи", "1073721742406713426": "Мандалорцы"}
    # @bot.slash_command(name="check_roles", description="Проверить роли участников и сохранить в JSON")
    # async def check_roles(ctx):
    #     guild = ctx.guild  # Получаем сервер, на котором вызвана команда
    #     with open('commands/clan_commands/clan_members.json', 'r',  encoding='utf-8') as f:  # Загружаем данные из JSON файла
    #         clan_data = json.load(f)
    #     # Проходим по всем участникам сервера
    #     for member in guild.members:
    #         if str(member.id) not in clan_data: # Добавляем данные для пользователя которого еще нет в системе
    #                 clan_data[str(member.id)] = { 
    #                     "main_server": True,  # Есть ли на сервере
    #                     "clan": False,  # Состояние в клане
    #                     "ea_name": False}
    #                 # Сохраняем обновленные данные в JSON-файл
    #                 with open('commands/clan_commands/clan_members.json', 'w', encoding='utf-8') as f:
    #                     json.dump(clan_data, f, indent=4, ensure_ascii=False) 
    #         # Проверяем, есть ли у участника одна из указанных ролей
    #         for role in member.roles:
    #             if str(role.id) in ROLES_TO_CHECK:
    #                 # Записываем ID участника и название роли
    #                 clan_data[str(member.id)]["clan"] = {ROLES_TO_CHECK[str(role.id)]: str(role.id)}
    #                 with open('commands/clan_commands/clan_members.json', 'w', encoding='utf-8') as f:
    #                     json.dump(clan_data, f, indent=4, ensure_ascii=False)
    #   await ctx.respond("Проверка ролей завершена. Данные сохранены в файл `members_with_roles.json`.", ephemeral=True)


with open('commands/clan_commands/clan_members.json', 'r',  encoding='utf-8') as f:  # Загружаем данные из JSON файла
    clan_data = json.load(f)
with open('commands/clan_commands/clan_list.json', 'r',  encoding='utf-8') as f:  # Загружаем данные из JSON файла
    clan_list = json.load(f)
from commands.moderator_commands.embend import Embend
from commands.moderator_commands.say import Say
from commands.moderator_commands.sync import Sync
from commands.clan_commands.clan import Clan
from commands.clan_commands.clan_join import Clan_join
from YTDLSourse import MusicCommands


mussic_commands_cog = MusicCommands(bot)
embend_cog = Embend(bot)
say_cog = Say(bot)
sync_cog = Sync(bot)
clan_cog = Clan(bot, clan_data, clan_list)
clan_join_cog = Clan_join(bot, clan_data, clan_list)



@bot.event
async def on_ready():
    print(f'{bot.user} готов и онлайн!')
    print("Зарегистрированные команды:")
    for command in bot.application_commands:
        print(f"- {command.name}")


load_dotenv()
token = os.getenv('DISCORD_TOKEN')
if token is None:
    print("Ошибка: токен не найден в файле .env")
    exit(1)
bot.run(token)
