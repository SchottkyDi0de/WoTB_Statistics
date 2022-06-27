import wotb_api
import discord
from time import sleep
from discord.ext import commands
from settings import bot_settings

class App():
    def __init__(self):
        self.bot = commands.Bot(command_prefix=bot_settings['command_prefix'])
        self.api = wotb_api.App()

    def main(self):
        @self.bot.command()
        async def id(ctx):
            data = ctx.message.content
            data = data.split(' ')
            
            try:
                player_name = data[1]
            except:
                await ctx.send('Ошибка, не указан ник игрока')
            else:
                player_id = self.api.get_id_for_name(player_name)
                
                if player_id == 'Error':
                    for i in self.api.errors:
                        errors = f'{i}\n'
                        await ctx.send(errors)
                
                await ctx.send(f'Игрок {self.api.c_player_name} имеет id: {player_id}')
            
        @self.bot.command()
        async def stats(ctx):
            data = ctx.message.content
            data = data.split(' ')
           
            try:
                player_name = data[1]
            except:
                await ctx.send('Ошибка, не указан ник игрока')
            else:
                player_stats = self.api.get_player_stat_for_name(player_name)
            
                if player_stats == 'Error':
                    for i in self.api.errors:
                        errors = f'{i}\n'
                        await ctx.send(errors)
                        continue
                
                await ctx.send(self.api.stats_descriptions)
            
        self.bot.run(bot_settings['token'])
        
if __name__ == '__main__':
    app = App()
    app.main()