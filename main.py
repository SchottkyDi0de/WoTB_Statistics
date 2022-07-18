'''
Main file of bot
Главный фаил бота
'''
import logging

import discord
from discord.ext import commands

import wotb_api
import settings
import messages as m
from embed_gen import Generate
from settings import bot_settings

logging.basicConfig(level=logging.FATAL)
bot = commands.Bot(command_prefix=bot_settings['command_prefix'])
bot.remove_command('help')

class App():
    '''
    Main class of bot
    Главный класс бота
    '''
    def __init__(self):
        self.emb_gen = Generate()
        self.err_msg = m.Error_MSG()
        self.info_msg = m.Info_MSG()
        self.api = wotb_api.API()
        self.__token = settings.bot_settings['TOKEN']

    def log(self,message,level=0):
        '''
        Функция для логированния в консоль.
        Уровни лога:
        0 - INFO      (по умолчанию)
        1 - WARNING
        2 - ERROR
        Уровни лога лишь условноть, определяющая
        внешний вид сообщения.
        '''
        log_level_list = [
        'INFO', 'WARNING', 'ERROR'
        ]
        msg_type = log_level_list[level]
        print(f'Log -> {msg_type}:{message}')

    def error_handler(self,data):
        '''
        Сопостовляем полученную ошибку со словарём
        и возвращаем True если данные совпадают
        со словарём ошибок.
        '''
        for i in self.api.error_list:
            if data == i:
                return True
        return False

    def main(self):
        '''
        Здесь описанна логика бота, и его взаимодействие
        с другими модулями
        '''
        @bot.command()
        async def stats(ctx):
            '''
            Обрабатываем комманду '!stats'
            '''
            command = ctx.message.content
            command = command.split(' ')
            self.log(f'Request {command}')

            if len(command) == 2:
                player_data = self.api.get_player_stats(command[1])
                if self.error_handler(player_data):
                    self.log('API Return error!',1)
                    await ctx.send(embed = self.
                                   err_msg.return_error_emb(player_data))
                else:
                    self.log('Answer is good')
                    embed = self.emb_gen.account_data(player_data,
                                                      self.api.last_id)
                    await ctx.send(embed = embed)

            elif len(command) == 3:
                player_data = self.api.get_player_stats(command[1],
                                                        command[2])
                if self.error_handler(player_data):
                    self.log('API Return error!',1)
                    await ctx.send(embed = self.
                                   err_msg.return_error_emb(player_data))
                else:
                    self.log('Answer is good')
                    embed = self.emb_gen.account_data(player_data,
                                                      self.api.last_id)
                    await ctx.send(embed = embed)

            elif len(command) > 3:
                self.log('Bot return error!',1)
                await ctx.send(embed = self.err_msg.return_error_emb('CFE'))
            else:
                self.log('Bot return error!',1)
                await ctx.send(embed = self.err_msg.return_error_emb('NN'))

        @bot.command()
        async def ver(ctx):
            '''
            Обрабатываем комманду '!ver'
            '''
            self.log('Request !ver')
            await ctx.send(embed = self.info_msg.return_about_embed())
            self.log('Answer is good')
            
        @bot.command()
        async def help(ctx):
            '''
            Обрабатываем комманду '!help'
            '''
            self.log('Request !help')
            await ctx.author.send(embed = self.info_msg.return_help_embed())
            self.log('Answer is good')

        @bot.command()
        async def server(ctx):
            '''
            Обрабатываем комманду '!server'
            '''
            command = ctx.message.content
            command = command.split(' ')
            self.log(f'Request {command}')

            if len(command) == 2:
                if command[1].lower() == 'all':
                    embed = ''
                    s_status = ''
                    s_status = self.api.get_server_status('all')
                    if self.error_handler(s_status):
                        self.log('API Return error!',1)
                        embed = self.err_msg.return_error_emb(s_status)
                        await ctx.send(embed = embed)
                    else:
                        self.log('Answer is good')
                        embed = self.emb_gen.server_status_all(s_status)
                        await ctx.send(embed = embed)

                else:
                    s_status = ''
                    embed = ''
                    s_status = self.api.get_server_status(command[1])
                    if self.error_handler(s_status):
                        self.log('API Return error!',1)
                        embed = self.err_msg.return_error_emb(s_status)
                        await ctx.send(embed = embed)
                    else:
                        self.log('Answer is good')
                        embed = self.emb_gen.server_status(s_status)
                        await ctx.send(embed = embed)

            elif len(command) == 1:
                s_status = self.api.get_server_status()
                if self.error_handler(s_status):
                    self.log('API Return error!',1)
                    await ctx.send(embed = self.err_msg.
                                   return_error_emb(s_status))
                else:
                    self.log('Answer is good')
                    await ctx.send(embed = self.emb_gen.
                                   server_status(s_status))
            else:
                self.log('Bot return error!',1)
                await ctx.send(embed = self.err_msg.return_error_emb('CFE'))

        self.log('Bot has been started!')
        bot.run(self.__token)

    def testing(self):
        '''
        Раздел для тестирования бота
        заменяет собой app.main() на время тестирования
        в конструкции if __name__ == "__main__"
        '''
        @bot.command()
        async def test(ctx):
            send = self.api.get_server_status('')
            embed = self.emb_gen.server_status(send)
            await ctx.send(embed = embed)

        print('Бот запущен!')
        bot.run(bot_settings['TOKEN'])

if __name__ == '__main__':
    app = App()
    app.main()
else:
    module_err_msg = \
    f'This file ({__name__}.py) is not a module\n\
    and is not meant to be imported'
    print(module_err_msg)
    quit()
