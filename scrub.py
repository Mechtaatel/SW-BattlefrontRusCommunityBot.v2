
# Создайте нового клиента и подключитесь к серверу
#client = #MongoClient(os.environ['mongo'])

#db = client.get_database('Rating_data_base')
#collection = db['Collection_data']
# Отправьте пинг, чтобы подтвердить успешное соединение


#@bot.event
#async def on_member_join(member):
 # check_author = collection.find_one({"_id": str(member.id)})
  #guild = member.guild  # Получить сервер, к которому присоединился участник
  #if guild.id == guild_id:
    # Добавляем роль только что присоединившемуся участнику
   # role = guild.get_role(rating_0)
    #await member.add_roles(role)
    #channel = guild.get_channel(1071600437209354241)
    #if check_author:
     # await channel.send(f'С возвращением, {member.mention}!')
    #else:
     # await member.send(f"""Привет, {member.mention}!
#Добро пожаловать на сервер. Пройдите регистрацию коммандой /reg.
#В пункте name Укажите свой никнейм из EA, в пункте hourse укажите время проведеннное 
#в игре."""
 #                       )
 #     await channel.send(f'Поприветсвуем нового участника, {member.mention}!')

  #else:
   # print('Не работает')

  #channel = guild.get_channel(1142846261196759071)
  # Замените YOUR_WELCOME_CHANNEL_ID фактическим идентификатором канала, на котором вы
  #хотите отправить приветственное сообщение
  #await channel.send(f'Welcome to the server, {member.mention}!')
  # Отправьте приветственное сообщение на указанный канал




# @bot.command()
# @commands.has_permissions(administrator=True)
import os
token = os.environ["token_discord_battlefront"]
print(token)