import discord
import os
from discord.ui import Button, View, Select, Modal, InputText
import json

class MyModal(Modal):
    def __init__(self, select_clan, clan_data, bot):
        super().__init__(title="Заполните форму")
        self.add_item(InputText(label="Ваш EA ник", placeholder="Обязательно"))
        self.select_clan = select_clan
        self.clan_data = clan_data
        self.bot = bot
    async def callback(self, interaction: discord.Interaction):
        ea_nick = self.children[0].value
    
        if str(interaction.user.id) not in self.clan_data:
            self.clan_data[str(interaction.user.id)] = { 
                    "main_server": bool(self.bot.get_guild(1071600435607113819).get_member(interaction.user.id)),  # Есть ли на сервере
                    "clan": False,  # Состояние в клане
                    "ea_name": ea_nick,
                    "Application": self.select_clan['name']}
        else:
            self.clan_data[str(interaction.user.id)]['ea_name'] = ea_nick
            self.clan_data[str(interaction.user.id)]["Application"] = self.select_clan['name']
        with open('commands/clan_commands/clan_members.json', 'w', encoding='utf-8') as f:
            json.dump(self.clan_data, f, indent=4, ensure_ascii=False)    
        embed = discord.Embed(title='Фракция',# Создаем Embed с предложением вступить в фракцию
                                       description=f"Ваша заявка в {self.select_clan['name']} отправлена",
                                       color=2829617)
        
        await interaction.response.send_message(embed=embed, view=None)
        leader_id = self.select_clan['Leader']
        try:
            leader = await self.bot.fetch_user(leader_id) # Получаем объект пользователя по ID
            notify_embed = discord.Embed(
                title="Новая заявка на вступление в клан",
                description=f"Пользователь {interaction.user.mention} подал заявку на вступление в клан **{self.select_clan['name']}**.\nEA-ник: **{ea_nick}**",
                color=0xFF0000
            )
            await leader.send(embed=notify_embed)
        except discord.NotFound:
            print(f'Не удалось найти лидера с ID{leader_id}')
        except discord.HTTPClient as e:
            print(f'Ошибка при отправке сообщения лидеру {e}')
class Clan:
    def __init__(self,bot, clan_data, clan_list):
        self.bot = bot
        self.setup()
        self.clan_data = clan_data
        self.clan_list = clan_list
        
    def setup(self):
        @self.bot.slash_command(name='clan', description="фракция")
        async def clan(ctx):

            if str(ctx.author.id) not in self.clan_data: # Добавляем данные для пользователя которого еще нет в системе
                guild = self.bot.get_guild(1071600435607113819) # Получаем сервер по ID
                main_member = guild and guild.get_member(ctx.author.id) is not None  # Проверяем, состоит ли пользователь на сервере
                self.clan_data[str(ctx.author.id)] = { 
                    "main_server": main_member,  # Есть ли на сервере
                    "clan": False,  # Состояние в клане
                    "ea_name": False,
                    "Application": None}
                # Сохраняем обновленные данные в JSON-файл
                with open('commands/clan_commands/clan_members.json', 'w', encoding='utf-8') as f:
                    json.dump(self.clan_data, f, indent=4)
            if self.clan_data[str(ctx.author.id)]['Application']:
                
                embed = discord.Embed(title="Фракция",
                                      description=f"Ваша заявка в **{self.clan_data[str(ctx.author.id)]['Application']}** все еще на рассмотрении",
                                      color=2829617)
                view = View()
                cancell_button = Button(label="Отозвать", style=discord.ButtonStyle.red)
                view.add_item(cancell_button)
                await ctx.respond(embed=embed, view=view, ephemeral=True)
                async def cancell_callback(interaction):
                    if interaction.user.id != ctx.author.id:
                        await interaction.response.send_message("Эти кнопки не для вас!", ephemeral=True)
                        return
                    self.clan_data[str(interaction.user.id)]['Application'] = None
                    embed = discord.Embed(title='Фракция', description='Ваша заявка отменена')
                    with open('commands/clan_commands/clan_members.json','w',encoding='utf-8') as f:
                        json.dump(self.clan_data,f,indent=4,ensure_ascii=False)
                    await interaction.response.edit_message(embed=embed, view=None)
                cancell_button.callback = cancell_callback
            else:
                if self.clan_data[str(ctx.author.id)]['clan'] == False: 
                    join_button = Button(label='Вступить во фракцию', style=discord.ButtonStyle.primary) # Создаем кнопку для вступления в фракцию
                    view = View() # Создаем View и добавляем кнопку
                    view.add_item(join_button)
                    embed = discord.Embed(title='Фракция',# Создаем Embed с предложением вступить в фракцию
                                        description='Вы не состоите во фракции. Хотите вступить?',
                                        color=2829617)
                    await ctx.respond(embed=embed, view=view, ephemeral=True)
                    async def join_callback(interaction):  # Обработка нажатия на кнопку 'Вступить во фракцию'
                        if interaction.user.id != ctx.author.id:
                            await interaction.response.send_message("Эти кнопки не для вас!", ephemeral=True)
                            return
                        
                        select = Select(placeholder='Выберете фракцию',
                            options = [discord.SelectOption(
                                label=f"{'🔒' if not clans['open'] else ''} {clans['name']} ",
                                value=str(index)) for index, clans in enumerate(self.clan_list['clans'])])
                        
                        select_view = View()
                        select_view.add_item(select)

                        embed = discord.Embed(title='Выберете Фракцию', description='Пожалуйста выберете фракцию из списка.', color=2829617)
                        await interaction.response.edit_message(embed=embed, view=select_view)

                        async def select_callback(interaction): #Обработка выбора
                            if interaction.user.id != ctx.author.id:
                                await interaction.response.send_message("Эти кнопки не для вас!", ephemeral=True)
                                return
                            selected_clan_index = int(select.values[0])
                            select_clan = self.clan_list['clans'][selected_clan_index]
                            if select_clan['open']:
                                if select_clan['role_id'] == "clones": # Сложная операция с выбором подразделения колонов
                                    embed = discord.Embed(title='Выберете подразделение', description='Пожалуйста выберете подразделение из списка.', color=2829617)
                                    select_clone = Select(placeholder='Выберете подразделение',
                                                    options=[discord.SelectOption(label='104-й Батальен', value='1221788406225567774'),
                                                            discord.SelectOption(label='181-я Танковая дивизия', value='1221779497129476096'),
                                                            discord.SelectOption(label='212-й Штурмовой батальен', value='1221790504417497178'),
                                                            discord.SelectOption(label='327-й Звездный корпус', value='1221791044031479891'),
                                                            discord.SelectOption(label='41-й Элитный корпус', value='1221791999921754252'),
                                                            discord.SelectOption(label='501-й Легион', value='1221792754699337818'),
                                                            discord.SelectOption(label='87-й Корпус часовых', value='1221795692901568532'),
                                                            discord.SelectOption(label='91-й Развед корпус', value='1221793633070743572'),
                                                            discord.SelectOption(label='332-я Рота', value='1222069531850051594'),
                                                            discord.SelectOption(label='Корусантский гвардеец', value='1221795964298334218')])
                                    select_view = View()
                                    select_view.add_item(select_clone)
                                    await interaction.response.edit_message(embed=embed, view=select_view)
                                    async def select_clone_callback(interaction): # Выбор подразделения клонов
                                        if interaction.user.id != ctx.author.id:
                                            await interaction.response.send_message("Эти кнопки не для вас!", ephemeral=True)
                                            return
                                        selected_option = next((option for option in select_clone.options if option.value == select_clone.values[0]), None)
                                        guild = self.bot.get_guild(1071600435607113819)
                                        member = guild.get_member(interaction.user.id)

                                        if member:
                                            role_standart = guild.get_role(1165749431455461437)
                                            await member.remove_roles(role_standart)
                                            role = guild.get_role(int(select_clone.values[0]))
                                            await member.add_roles(role)  # Выдаем роль
                                            embed = discord.Embed(title='Фракция', description=f'Вы успешно вступили в {selected_option}!', color=2829617)
                                            self.clan_data[str(interaction.user.id)]['clan'] = {selected_option.label: select_clone.values[0]}
                                        else:
                                            embed = discord.Embed(title='Фракция', description=f'Вы успешно вступили в {selected_option}!', color=2829617)
                                            self.clan_data[str(interaction.user.id)]['clan'] = {selected_option.label: select_clone.values[0]}
                                        with open('commands/clan_commands/clan_members.json', 'w',  encoding='utf-8') as f:
                                            json.dump(self.clan_data,f,indent=4,ensure_ascii=False)
                                        await interaction.response.edit_message(embed=embed, view=None)
                                    select_clone.callback = select_clone_callback

                                else: # Обработка выбора не клоновов
                                    guild = self.bot.get_guild(1071600435607113819)  # Получаем сервер
                                    member = guild.get_member(interaction.user.id)  # Получаем объект Member
                                    if member:
                                        role_standart = guild.get_role(1165749431455461437) # получаем стандартную роль
                                        await member.remove_roles(role_standart) # отбираем
                                        role = guild.get_role(int(select_clan['rank'][0]['rank_1'][1] if select_clan['rank'] else select_clan['role_id'])) # получаем роль что выбрал игрок
                                        await member.add_roles(role)  # Выдаем роль
                                    selected_option = next((option for option in select.options if option.value == select.values[0]), None)
                                    embed = discord.Embed(title='Фракция', description=f'Вы успешно вступили в {selected_option}!', color=2829617)
                                    self.clan_data[str(interaction.user.id)]['clan'] = {selected_option.label: select_clan['rank'][0]['rank_1'][1] if select_clan['rank'] else select_clan['role_id']}
                                    with open('commands/clan_commands/clan_members.json', 'w', encoding='utf-8') as f:
                                        json.dump(self.clan_data,f,indent=4,ensure_ascii=False)
                                    embed = discord.Embed(title='Фракция', description=f'Вы успешно вступили в {selected_option}!', color=2829617)
                                    await interaction.response.edit_message(embed=embed, view=None)
                            else:
                                modal = MyModal(select_clan, self.clan_data, self.bot)
                                await interaction.response.send_modal(modal) # Отправляем модальное окно
                        select.callback = select_callback
                    join_button.callback = join_callback

                else: # Функция выхода из фракции
                    embed = discord.Embed(title="фракцию", description="вы уже состоите в фракции!", color=2829617)
                    view = View()
                    exit_button = Button(label='Покинуть фракцию?', style=discord.ButtonStyle.red)
                    view.add_item(exit_button)
                    await ctx.respond(embed=embed, view=view)

                    async def exit_callback(interaction):
                        if interaction.user.id == ctx.author.id:
                            if self.clan_data[str(ctx.author.id)]["main_server"]:
                                guild = self.bot.get_guild(1071600435607113819)  # Получаем сервер
                                member = guild.get_member(interaction.user.id)  # Получаем объект Member
                                if member:
                                    role = guild.get_role(int(list(self.lan_data[str(ctx.author.id)]['clan'].values())[0]))
                                    await member.remove_roles(role)
                                    role_standart = guild.get_role(1165749431455461437)
                                    await member.add_roles(role_standart)
                                else:
                                    self.clan_data[str(ctx.author.id)]["main_server"] = False

                            self.clan_data[str(ctx.author.id)]['clan'] = False
                            with open('commands/clan_commands/clan_members.json','w',  encoding='utf-8') as f:
                                json.dump(self.clan_data,f, indent=4)
                            embed = discord.Embed(title='Фракция', description='Вы успешно покинули фракцию!', color=2829617)
                            await interaction.response.edit_message(embed=embed, view=None)
                        else:
                            await interaction.response.send_message('Эта кнопка не для вас!', ephemeral=True)
                    exit_button.callback = exit_callback