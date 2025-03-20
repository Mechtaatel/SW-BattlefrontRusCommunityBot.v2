import discord
from discord.ui import Button, View, Modal, InputText

class MyModal(Modal):
    def __init__(self):
        super().__init__(title="Введите данные")
        self.add_item(InputText(label="Имя", placeholder="Ваше имя"))
        self.add_item(InputText(label="Возраст", placeholder="Ваш возраст"))
        
    async def callback(self, interaction: discord.Interaction):
        name = self.children[0].value  # Получаем значение из первого поля
        age = self.children[1].value   # Получаем значение из второго поля
        await interaction.response.send_message(f"Вы ввели: Имя - {name}, Возраст - {age}", ephemeral=True)
    
    # Класс для View с кнопками
class MyView(View):
    def __init__(self):
        super().__init__()

        # Кнопка "Открыть форму"
    @discord.ui.button(label="Открыть форму", style=discord.ButtonStyle.primary)
    async def button_callback(self, button: Button, interaction: discord.Interaction):
        modal = MyModal()
        await interaction.response.send_modal(modal)

# Команда для вызова Embed с кнопками
class Info:
    def __init__(self, bot):
        self.bot = bot
        self.setup()
    def setup(self):
        @self.bot.slash_command(name="info", description="Показать информацию с кнопками")
        async def info(ctx):
            embed = discord.Embed(
                title="Информация",
                description="Нажмите кнопку ниже, чтобы открыть форму.",
                color=0x00ff00
            )
            view = MyView()
            await ctx.respond(embed=embed, view=view)