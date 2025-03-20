import discord
from discord.ui import Button, View, Select
import json

class Clan_join:
    def __init__(self, bot, clan_data, clan_list):
        self.bot = bot
        self.setup()
        self.clan_list = clan_list
        self.clan_data = clan_data
    def setup(self):
        @self.bot.slash_command(name='clan_join', description='Список заявок на вступление в клан')
        async def clan_joun(ctx):
            Leader_clan = None
            for clan in self.clan_list['clans']:
                if str(ctx.author.id) == str(clan['Leader']):
                    Leader_clan = clan['name']
                    break
            if not Leader_clan:
                await ctx.respond('Вы не являетесь лидером какого либо клана!', ephemeral=True)
                return
            applications = []
            for user_id, data in self.clan_data.items():
                if data.get('Application') == Leader_clan:
                    applications.append((user_id, data['ea_name']))
            if not applications:
                await ctx.respond(f'Нет заявок на вступление в клан **{Leader_clan}**.', ephemeral=True)
                return


            select = Select(
                placeholder="Выберите заявку",
                options=[
                    discord.SelectOption(label=f'<@{user_id}>({ea_name})',value=user_id) for user_id, ea_name in applications
                    ]
                )
            
            accept_button = Button(label='Принять', style=discord.ButtonStyle.green, custom_id='accept_button')
            reject_button = Button(label='Отклонить', style=discord.ButtonStyle.red, custom_id='reject')

            view = View()
            view.add_item(select)
            view.add_item(accept_button)
            view.add_item(reject_button)
            applications_text = "\n".join(
                f'#{i}. <@{user_id}>\nEA-ник **{ea_name}**'
                for i, (user_id, ea_name) in enumerate(applications, 1) or 'Заявки отсутствуют.'
            )
            embed = discord.Embed(
                title=f'Заявки в клан {Leader_clan}',
                description=f"Выберете заявку из списка ниже и нажмите кнопку для действия:\n\n{applications_text}",
                color=2829617
            )
            
            selected_user_id = [None] # Сохраняем выбранного пользователя
            async def select_callback(interaction):
                if interaction.user.id != ctx.author.id:
                    await interaction.response.send_message("Это не для вас!", ephemeral=True)
                    return
                selected_user_id[0] = interaction.data['values'][0]
                await interaction.response.defer() # Откладываем ответ, чтобы не было ошибки
            
            async def button_callback(interaction):
                if interaction.user.id != ctx.author.id:
                    await interaction.response.send_message("Эти кнопки не для вас!", ephemeral=True)
                    return
                if not selected_user_id[0]:
                    await interaction.response.send_message('Сначала выберете заявку')
                    return
                user_id = selected_user_id[0]
                if user_id not in self.clan_data or self.clan_data[user_id]['Application'] != Leader_clan:
                    await interaction.response.send_message('Заявка уже обработана и удалена')
                if interaction.data['custom_id'] =='accept':
                    self.clan_data[user_id]['clan'] = {self.clan_list['clans'][next(i for i, c in enumerate(self.clan_list['clans']) if c['name'] == Leader_clan)]['role_id']}
                    self.clan_data [user_id]['Application'] = None
                    guild = self.bot.get_guild(1071600435607113819)
                    member = guild.get_member(int(user_id))
                    if member:
                        role_standart = guild.get_role(1165749431455461437)
                        await member.removes(role_standart)
                        role = guild.get_role(int(self.clan_data[user_id]['clan'][Leader_clan]))
                        await member.add_roles(role)
                    await interaction.response.send_message(f'Заявка <@{user_id}> принята в кlan **{Leader_clan}**!', ephemeral=True)
                elif interaction.data['custom_id'] == 'reject':
                    self.clan_data[user_id]['Application'] = None
                    await interaction.response.send_message(f"Заявка <@{user_id}> отклонена.", ephemeral=True)
                with open('commands/clan_commands/clan_members.json', 'w', encoding='utf-8') as f:
                    json.dump(self.clan_data,f,indent=4,ensure_ascii=False)
            select.callback = select_callback
            accept_button.callback = button_callback
            reject_button.callback = button_callback

            await ctx.respond(embed=embed, view=view, ephemeral=True)