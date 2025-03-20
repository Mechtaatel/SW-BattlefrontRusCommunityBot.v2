
@bot.command(name='switche', description='')
async def switch(ctx, role: str):

    check_author = collection.find_one({"_id": str(ctx.author.id)})
    if check_author:
        if role == 'Light':
            await ctx.respond('Вернуться уже не получится)')
            guild = bot.get_guild(guild_id)
            obj = role_commands(ctx, check_author, guild, role)
            await obj.switch()
    else:
        await ctx.respond('Вы не зарегестрированы, воспользуйтесь командой /reg')



