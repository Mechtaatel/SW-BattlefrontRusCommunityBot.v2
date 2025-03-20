
@bot.command()
@commands.has_permissions(administrator=True)
async def reup(ctx, member: discord.Member):
    db = client.get_database('Rating_data_base')
    collection = db['Collection_data']
    intcollecion = collection.find_one({"_id"})
    print(intcollecion)
