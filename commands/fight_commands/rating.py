
@bot.command(name='rating', description='Узнать свой рейтинг')
async def rating(ctx):
    member = ctx.user
    check_author = collection.find_one({"_id": str(member.id)})
    if check_author:
        await ctx.respond(f"""Режим 4 на 4:`{check_author['Rating_4v4']}`
    Режим 2 на 2:`{check_author['Rating_2v2']}`
    Режим 1 на 1:`{check_author['Rating_1v1']}`""")
    else:
        await ctx.respond('Вы не зарегистрированы')