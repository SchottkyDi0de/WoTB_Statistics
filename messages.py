import wotb_api
from discord import Embed
#from discord import Color

_empty_embed_dict = {
"title": "",
"color": 00000000,
"description": "",
"timestamp": "",
"author": {
    "name": "[HVOLT] WoTB Statistics"},
"image": {},
"thumbnail": {
    'url' : ''},
"footer": {
"text": ""},
"fields": []}
        
_emb_colors = {
'red' : 16711680,
'blue' : 293846,
'orange' : 14059038,
'purple' : 12464383}

_error_description = {
'IN' : '❗ Длинна никнейма должна быть хотя бы 3 символа',
'IS' : '''❗ Некорректный запрос,
Никнейм может состоять из:
Латиннских букв A-Z и нижнего подчёркивания "_"''',
'SNS' : '''❗ Некорректный запрос,
Никнейм может состоять из:
Латиннских букв A-Z и нижнего подчёркивания "_"''',
'AE' : '❌ Внутреняя ошибка API ',
'PNF' : '❌ Игрок с данным именем не найден ',
'ED' : '❌ Нет данных о данном игроке ',
'NN' : '❗ Укажите никнейм игрока ',
'CFE' : '❗ Нераспознанный формат команды'}

class Error_MSG():
    '''
    Класс создающий сообщения об ошибках
    '''
    def __init__(self):
        api = wotb_api.API()
        self.error_dict = api.error_dict
        self.error_image = 'https://i.ibb.co/bg7ftRL/logo-symbol-attention-png-6200bfcb0e6488d2b48f6a77a03ded90.png'
        
    def return_error_emb(self,error):
        '''
        Создаём embed объект с описанием ошибки
        '''
        emb_dict = _empty_embed_dict
        emb_dict['title'] = f'Ошибка: {self.error_dict[error]}'
        emb_dict['color'] = _emb_colors['red']
        emb_dict['description'] = _error_description[error]
        emb_dict['footer']['text'] = '🔸 Будьте внимателней при вводе команды'
        emb_dict['thumbnail']['url'] = self.error_image
        err_emb = Embed.from_dict(emb_dict)
        return err_emb

class Info_MSG:
    '''
    Класс создающий информационные сообщения
    '''
    def __init__(self):
        self.old_bot_version = '0.1.0'
        self.bot_version = '0.1.2'
        
    def return_help_embed(self):
        help_text = f'''
Команды для бота WoTB Statistics
Префикс команд у данного бота: **!**
Версия бота: {self.bot_version}

__**Команда:**__
> !stats [NickName*] [region]
Имеет два аргумеета, никнейм и регион.
* - обязательный аргумент

__**Описание:**__
Данная команда позволяет вам получить 
подробную статистику игрока, чей
никнейм вы укажете. Регион поиска по
умолчанию RU но его можно изменить в ручную,
указав аргумент [region]
**Пример использования команды:**
> !stats player
- Бот отправит подробную характеристику
игрока player
> !stats player na
- Бот отправит подробную характеристику
игрока ded, чей аккаунт зарегестрирован на NA
сервере.

__**Команда:**__
> !ver

__**Описание:**__
Выведет информацию о боте

__**Команда:**__
> !server [region]

__**Описание:**__
Выведет статистику сервера, если указать 
регион, то выведется статистика сервера 
в другом, указанном вам регионе. 
Если в аргумент [region] поместить 
неверное значение, то регион 
установится RU. Если в аргумент 
[region] передать all то выведется 
статистика всех 4-х серверов на всех
регионах.

__**Пример использования команды:**__
> !server
- Бот отправит вам статистику RU сервера
> !server eu
- Бот отправит вам статистику EU сервера
(Европейский сервер)
> !server all
- Бот отправит вам статистику всех 4 серверов.

__**Подробнее про регионы:**__
У WoT Blitz есть всего 4 сервера, каждый
находится в своём регионе.
__RU__ - СНГ
__EU__ - Европа
__NA__ - Америка
__ASIA__ - Азия
если хотите указать сервер, выбирайте
один из представленных выше серверов, и
добавляйте его в качестве аргумента к 
команде, как показанно в примерах.
__**Особенности команд**__
1. Команды чувствительны к регистру. 
пишите команды строго в нижнем регистре
> !stats, !ver, !server
2. Все аргументы команд не чувствительны
к регистру:
__**Пример:**__
Команда:
> !stats player asia
будет работать также как и:
> !stats PlaYer AsIa
'''
        emb_dict = _empty_embed_dict
        emb_dict['description'] = help_text
        emb_dict['title'] = 'Help лист'
        emb_dict['color'] = _emb_colors['purple']
        emb_dict['footer']['text'] = '🔸 Нашли ошибку? Сообщите разработчику бота!'
        embed = Embed.from_dict(emb_dict)
        return embed

    def return_about_embed(self):
        '''
        Создаём embed объект который хранит в себе
        информацию о боте.
        '''
        about = f'''🔒 Статус: Альфа тест
🔑 Версия: {self.bot_version}
📀 Автор: _Zener#1024
```python
------UPDATE_LOG------
ver: {self.old_bot_version} -> {self.bot_version}
> Code refactoring
> Now the code matches 'PEP8'
> Correction of syntax errors
> Add new stats 'battles_per_day'
```'''
        about_emb = _empty_embed_dict
        about_emb['title'] = 'Информация о боте'
        about_emb['color'] = 13201920
        about_emb['description'] = about
        about_emb['footer']['text'] = '🔸 Иногда выходят обновления xD'
        embed = Embed.from_dict(about_emb)
        return embed
