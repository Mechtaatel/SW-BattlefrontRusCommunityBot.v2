@bot.command(description="Регистрация. В пункте Name: введите свой ник.В пункте hourse введите сколько у вас часов")
async def reg(ctx, name: str, hourse: int):
    if hourse <= 50:
        rating = 200
    elif hourse <= 300:
        rating = 400
    elif hourse <= 4000:
        rating = 600
    else:
        rating = 1000

    db = client.get_database('Rating_data_base')
    collection = db['Collection_data']
    # listdb_users = db.Rating_data_base.find({})
    # list_db_users = list(listdb_users)
    # idUsers = list_db_users[0]

    # и `user_id` это id пользователя (ctx.author.id)

    # преобразуем в строку, поскольку в JSON ключи являются строками
    user_id = str(ctx.author.id)
    # Создаем запрос в MongoDB для поиска пользователя по id.
    user_document = collection.find_one({"_id": user_id})

    # Проверяем найден ли id пользователя в базе данных
    if user_document:
        # Получить доступ к `EA_Name` непосредственно из `user_document`
        EAName = user_document['EA_Name']
        await ctx.respond(f'Вы уже зарегестрированы под никнемом {EAName}.')

    else:

        #async def check_name_in_database(ctx,db, name):
        # Проверяем найден ли name пользователя в базе данных
        user_document1 = collection.find_one({"EA_Name": name})
        if user_document1:
            await ctx.respond(f"""Имя {name} уже занято пользователем.
    Обратитесь пожалуйста в Администрацию.""")
            return
        else:
            guild = bot.get_guild(guild_id)
            member = ctx.user
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

                collection.update_one({'_id': user_id}, {"$set": new_data}, upsert=True)
                await ctx.respond(
                    """Поздравляем вы зарегестрированы. Воспользуйтесь командой /help что бы узнать основные команды."""
                )