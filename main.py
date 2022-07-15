import wotb_api
import messages as m
import settings
import discord
from discord import Webhook, RequestsWebhookAdapter
from discord.ext import commands
from settings import bot_settings
from parser import pars

class App():
    def __init__(self):
        self.bot = commands.Bot(command_prefix=bot_settings['command_prefix'])
        self.api = wotb_api.API()
        self.pars = pars()
        self.msg = m.msg()
        
    def error_handler(self,data):
        for i in self.api.error_list:
            if data == i:
                return True
                print(f'err: {i}')
        return False

    def main(self):
        @self.bot.command()
        async def stats(ctx):
            command = ctx.message.content
            command = command.split(' ')
            print(f'Запрос: {command}')
            if len(command) == 2:
                player_data = self.api.get_player_stats(command[1])
                if self.error_handler(player_data):
                    await ctx.send(embed = self.msg.return_error_emb(player_data))
                else:
                    embed = self.pars.get_data(player_data,self.api.last_id)
                    await ctx.send(embed = embed)
                    
            elif len(command) == 3:
                player_data = self.api.get_player_stats(command[1],
                                                        command[2])
                if self.error_handler(player_data):
                    await ctx.send(embed = self.msg.return_error_emb(player_data))
                else:
                    embed = self.pars.get_data(player_data,self.api.last_id)
                    await ctx.send(embed = embed)
                    
            elif len(command) > 3:
                await ctx.send(embed = self.msg.return_error_emb('CFE'))
            else:
                await ctx.send(embed = self.msg.return_error_emb('NN'))
                
        @self.bot.command()
        async def ver(ctx):
            await ctx.send(embed = self.msg.about_embed())
            
        @self.bot.command()
        async def server(ctx):
            command = ctx.message.content
            command = command.split(' ')
            
            if len(command) == 2:
                if command[1].lower() == 'all':
                    s_status = ''
                    s_status = self.api.get_server_status('all')
                    if self.error_handler(s_status):
                        embed = ''
                        embed = self.msg.return_error_emb(s_status)
                        await ctx.send(embed = embed)
                    else:
                        embed = ''
                        embed = self.pars.server_status_all(s_status)
                        await ctx.send(embed = embed)
                        
                else:
                    s_status = ''
                    s_status = self.api.get_server_status(command[1])
                    if self.error_handler(s_status):
                        embed = ''
                        embed = self.msg.return_error_emb(s_status)
                        await ctx.send(embed = embed)
                    else:
                        embed = ''
                        embed = self.pars.server_status(s_status)
                        await ctx.send(embed = embed)
                             
            elif len(command) == 1:
                s_status = self.api.get_server_status()
                if self.error_handler(s_status):
                    await ctx.send(embed = self.msg.return_error_emb(s_status))
                else:
                    await ctx.send(embed = self.pars.server_status(s_status))
            
            else:
                await ctx.send(embed = self.msg.return_error_emb('CFE'))
                
        print('Бот запущен!')
        self.bot.run(bot_settings['TOKEN'])
    
    def testing(self):
        @self.bot.command()
        async def test(ctx):
            send = self.api.get_server_status('')
            embed = self.pars.server_status(send)
            await ctx.send(embed = embed)
        
        
        
        
        
        print('Бот запущен!')
        self.bot.run(bot_settings['TOKEN'])

if __name__ == '__main__':
    app = App()
    app.main()
    
#@self.bot.command()
#        async def stats(ctx):
#            nickname = ctx.message.content
#            nickname = nickname.split(' ')
#            
#            if len(nickname) != 2:
#                await ctx.send(self.msg.errors['NN'])
#            else:
#                print(f'Bot request: {nickname}')
#                player_id = self.api.(nickname[1])
#                
#                if self.error_handler(player_id):
#                    self.webhook.send('',username=self.webhook_username,\
#                    embed=self.msg.return_error_emb(player_id))
#                else:
#                    data = self.api.player_stats_for_id(player_id)
#                    stats = self.pars.get_data(data, player_id)
#                    self.webhook.send('',username=self.webhook_username,embed=stats)
#                    
#                    
#        @self.bot.command()
#        async def ver(ctx):
#            print('Bot request: Bot info')
#            embed = self.msg.about_embed()
#            self.webhook.send('',username=self.webhook_username,embed=embed)
#            
#        @self.bot.command()
#        async def server(ctx):
#            command = ctx.message.content
#            command = command.split(' ')
#            
#            if len(command) == 2:
#                data = self.api.server_status(command[1])
#            else:
#                data = self.api.server_status()
#                
#            if self.error_handler(data):
#                print('Error:',data)
#                self.webhook.send('',username=self.webhook_username,\
#                embed=self.msg.return_error_emb(data))    
#            else:
#                status = self.pars.server_status(data)
#                self.webhook.send('',username=self.webhook_username,embed=status)
#                        
#        
#        print('Bot started!')
#        self.bot.run(bot_settings['TOKEN'])
#        
