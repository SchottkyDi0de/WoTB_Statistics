import wotb_api
import messages as m
import settings
#import discord
from discord import Webhook, RequestsWebhookAdapter
from discord.ext import commands
from settings import bot_settings
from parser import pars

class App():
    def __init__(self):
        self.bot = commands.Bot(command_prefix=bot_settings['command_prefix'])
        self.api = wotb_api.get()
        self.pars = pars()
        self.webhook_username = '[HVOLT] BOT Assistant'
        self.webhook = Webhook.from_url(settings.WEBHOOK_URL, adapter=RequestsWebhookAdapter())
        self.msg = m.msg()
        
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
                await ctx.send(self.msg.errors['NN'])
            else:
                print(f'Bot request: {nickname}')
                player_id = self.api.player_id(nickname[1])
                
                if self.error_handler(player_id):
                    self.webhook.send('',username=self.webhook_username,\
                    embed=self.msg.return_error_emb(player_id))
                else:
                    data = self.api.player_stats_for_id(player_id)
                    stats = self.pars.get_data(data, player_id)
                    self.webhook.send('',username=self.webhook_username,embed=stats)
                    
                    
        @self.bot.command()
        async def ver(ctx):
            print('Bot request: Bot info')
            embed = self.msg.about_embed()
            self.webhook.send('',username=self.webhook_username,embed=embed)
            
        @self.bot.command()
        async def server(ctx):
            data = self.api.server_status()
            print('Bot request: Server status')
            if self.error_handler(data):
                print('Error:',data)
                self.webhook.send('',username=self.webhook_username,\
                embed=self.msg.return_error_emb(data))    
            else:
                status = self.pars.server_status(data)
                self.webhook.send('',username=self.webhook_username,embed=status)
                    
        
        print('Bot started!')
        self.bot.run(bot_settings['TOKEN'])
        
if __name__ == '__main__':
    app = App()
    app.main()