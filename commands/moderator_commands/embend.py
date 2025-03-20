import discord
import json
from discord.ext import commands

class Embend:
    def __init__(self, bot):
        self.bot = bot
        self.setup()

    def parse_embed_json(self, json_file):
        embeds_json = json.loads(json_file)['embeds']

        for embed_json in embeds_json:
            embed = discord.Embed.from_dict(embed_json)
            yield embed
    
    def setup(self):
        @self.bot.command(name='embed', description='Отправить embed сообщение')
        @commands.has_permissions(administrator=True)
        async def add_embed(ctx, name: str):
            
            if name == 'help':
                with open("embed/help.json", "r") as file:
                    temp_ban_embeds = self.parse_embed_json(file.read())

                for embed in temp_ban_embeds:
                    await ctx.send(embed=embed)
            elif name == 'rule':
                with open("embed/rule.json", "r") as file:
                    temp_ban_embeds = self.parse_embed_json(file.read())
                    for embed in temp_ban_embeds:
                        await ctx.send(embed=embed)
            elif name == 'upgrade':
                with open("embed/serverupgrade.json", "r") as file:
                    temp_ban_embeds = self.parse_embed_json(file.read())
                    for embed in temp_ban_embeds:
                        await ctx.send("@everyone",embed=embed)
            elif name == 'partners':
                with open("commands/moderator_commands/embed/partners.json", "r") as file:
                    temp_ban_embeds = self.parse_embed_json(file.read())
                    for embed in temp_ban_embeds:
                        await ctx.send(embed=embed)
