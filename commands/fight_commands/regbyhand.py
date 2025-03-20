@bot.command(name='reg_byhand',description='Регистрация пользоваетля в ручную')
@commands.has_permissions(administrator=True)
async def regbyhand(ctx, name: str, rating: int, member: discord.Member):

    db = client.get_database('Rating_data_base')
    collection = db['Collection_data']
    # listdb_users = db.Rating_data_base.find({})
    # list_db_users = list(listdb_users)
    # idUsers = list_db_users[0]

    # Создаем запрос в MongoDB для поиска пользователя по id.
    user_document = collection.find_one({"_id": str(member.id)})

    # Проверяем найден ли id пользователя в базе данных
    if user_document:
        # Получить доступ к `EA_Name` непосредственно из `user_document`
        EAName = user_document['EA_Name']
        await ctx.respond(f'Пользователь уже зарегестрированы под никнемом {EAName}.')

    else:

        #async def check_name_in_database(ctx,db, name):
        # Проверяем найден ли name пользователя в базе данных
        user_document1 = collection.find_one({"EA_Name": name})
        if user_document1:
            await ctx.respond(f"Имя {name} уже занято пользователем")
            return
        else:
            guild = bot.get_guild(guild_id)
            roles = member.roles
            role = roles[len(roles) - 1]

            with open('Rating_commands/Role.json', 'r') as f:
                vipRole = json.load(f)

            if role.id == 1197490336075890718:
                role = roles[len(roles) - 2]
            elif role.id not in vipRole['VIP']:
                await member.remove_roles(role)
                await member.add_roles(guild.get_role(1071604948476895263))
                new_data = {
                    'EA_Name': name,
                    'Rating_1v1': rating,
                    'Rating_2v2': rating,
                    'Rating_4v4': rating,
                    'Ban': 'off'
                }

                collection.update_one({'_id': str(member.id)}, {"$set": new_data},
                                        upsert=True)
                await ctx.respond(f"Пользоваетль {member} зарегестрирован.")