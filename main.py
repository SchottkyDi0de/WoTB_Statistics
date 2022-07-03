import wotb_api
import messages as m
#import discord
from discord.ext import commands
from settings import bot_settings
from parser import pars

class App():
    def __init__(self):
        self.bot = commands.Bot(command_prefix=bot_settings['command_prefix'])
        self.api = wotb_api.get()
        self.pars = pars()
        
    def error_handler(self,data):
        for i in self.api.error_list:
            if data == i:
                return True
        return False

    def main(self):
        @self.bot.command()
        async def stats(ctx):
            nickname = ctx.message.content
            nickname = nickname.split(' ')
            
            if len(nickname) != 2:
                await ctx.send(m.errors['NN'])
            else:
                print(f'Bot request: {nickname}')
                player_id = self.api.player_id(nickname[1])
                if self.error_handler(player_id):
                    await ctx.send(m.errors[player_id])
                else:
                    data = self.api.player_stats_for_id(player_id)
                    stats = self.pars.get_data(data, player_id)
                    await ctx.send(stats)
                    
        @self.bot.command()
        async def ver(ctx):
            print('Bot request: Bot info')
            await ctx.send(m.about)
            
        @self.bot.command()
        async def server(ctx):
            data = self.api.server_status()
            print('Bot request: Server status')
            if self.error_handler(data):
                print('Errror:',data)
                await ctx.send(m.errors[data])
            else:
                status = self.pars.server_status(data)
                await ctx.send(status)
            
        
        print('Bot started!')
        self.bot.run(bot_settings['TOKEN'])
        
if __name__ == '__main__':
    app = App()
    app.main()