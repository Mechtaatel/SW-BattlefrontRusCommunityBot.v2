import discord
import asyncio
import yt_dlp as youtube_dl
import os
from discord.player import AudioSource, FFmpegPCMAudio

# Настройки для youtube_dl
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s',  # Используем только название и расширение
    'restrictfilenames': True,       # Убираем недопустимые символы
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'executable': 'C:/ffmpeg/bin/ffmpeg.exe',  # Укажите полный путь к ffmpeg.exe
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

queue = []

# Кастомный класс для FFmpegPCMAudio
class CustomFFmpegPCMAudio(discord.FFmpegPCMAudio):
    def __init__(self, source, *, data, volume=0.5, **kwargs):
        super().__init__(source, **kwargs)  # Передаем kwargs в родительский класс
        self.data = data
        self.filename = source  # Сохраняем имя файла для последующего удаления

    def cleanup(self):
        try:
            if hasattr(self, '_process'):
                super().cleanup()
            if hasattr(self, 'filename') and os.path.exists(self.filename):
                os.remove(self.filename)  # Удаляем временный файл
        except Exception as e:
            print(f"Ошибка при очистке FFmpeg: {e}")

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(CustomFFmpegPCMAudio(filename, data=data, **ffmpeg_options), data=data)
    
    @classmethod
    async def get_info(cls, url, *, loop=None):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        return data


class MusicCommands:
    def __init__(self, bot):
        self.bot = bot
        self.setup()

    def setup(self):
        async def play_next(ctx):
            if queue:
                data = queue.pop(0)  # Получаем первый трек из очереди

                voice_channel = ctx.guild.voice_client  # Воспроизводим трек
                player = await YTDLSource.from_url(data['url'], loop=self.bot.loop)
                voice_channel.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), self.bot.loop))

                await ctx.send(f'**Сейчас играет:** {data["title"]}')
            else:
                await ctx.send("Очередь пуста.")

        @self.bot.slash_command(name='leave', help='Бот покидает голосовой канал')
        async def leave(ctx):
            voice_client = ctx.guild.voice_client
            if voice_client.is_connected():
                await voice_client.disconnect()
            else:
                await ctx.send("Бот не подключен к голосовому каналу.")

        @self.bot.slash_command(name='play', help='Воспроизводит указанный трек или плейлист')
        async def play(ctx, url):
            try:
                if not ctx.author.voice:  # Проверяем, подключен ли пользователь к голосовому каналу
                    await ctx.send(f"{ctx.author.name} не подключен к голосовому каналу")
                    return
                channel = ctx.author.voice.channel  # Получаем голосовой канал пользователя
                voice_channel = ctx.guild.voice_client  # Получаем голосовое подключение бота
                if not voice_channel or not voice_channel.is_connected():  # Если бот не подключен к голосовому каналу, подключаемся
                    voice_channel = await channel.connect()
                data = await YTDLSource.get_info(url, loop=self.bot.loop)  # Извлекаем информацию о треке или плейлисте
                print(data)
                if 'entries' in data:  # Если это плейлист, добавляем все треки в очередь
                    for entry in data['entries']:
                        queue.append(entry)
                    await ctx.send(f"Добавлено {len(data['entries'])} треков в очередь.")
                else:
                    queue.append(data)  # Если это одиночный трек, добавляем его в очередь
                    await ctx.send(f"Добавлен трек: {data['title']}")
                if not voice_channel.is_playing():  # Если бот не воспроизводит музыку, начинаем воспроизведение
                    await play_next(ctx)
            except Exception as e:
                await ctx.send(f"Произошла ошибка: {str(e)}")

        @self.bot.slash_command(name='pause', help='Приостанавливает воспроизведение')
        async def pause(ctx):
            voice_client = ctx.guild.voice_client
            if voice_client.is_playing():
                await ctx.send("Воспроизведение приостановлено")
                voice_client.pause()
            else:
                await ctx.send("В данный момент ничего не играет.")

        @self.bot.slash_command(name='resume', help='Возобновляет воспроизведение')
        async def resume(ctx):
            voice_client = ctx.guild.voice_client
            if voice_client.is_paused():
                await ctx.send("Воспроизведение возобновлено")
                voice_client.resume()
            else:
                await ctx.send("Воспроизведение не приостановлено.")

        @self.bot.slash_command(name='stop', help='Останавливает воспроизведение')
        async def stop(ctx):
            voice_client = ctx.guild.voice_client
            if voice_client.is_playing():
                await ctx.send("Воспроизведение остановлено")
                voice_client.stop()
            else:
                await ctx.send("В данный момент ничего не играет.")