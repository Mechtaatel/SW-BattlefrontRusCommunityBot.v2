@bot.command(name='name', description='Узнать nickname участника')
async def name(ctx, member: discord.Member):
    check_author = collection.find_one({"_id": str(member.id)})
    if check_author:
        await ctx.respond(f"`{check_author['EA_Name']}`")
    else:
        await ctx.respond(f'Участник `{member.name}` не зарегистрирован')
