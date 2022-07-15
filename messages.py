import wotb_api
from discord import Embed
#from discord import Color

class msg():
    def __init__(self):
        api = wotb_api.API()
        self.error_dict = api.error_dict
        self.error_image = 'https://i.ibb.co/bg7ftRL/logo-symbol-attention-png-6200bfcb0e6488d2b48f6a77a03ded90.png'
        self.emb_colors = {
        'red' : 16711680,
        'blue' : 293846,
        'orange' : 14059038}
        self.empty_embed_dict = {
        "title": "",
        "color": 00000000,
        "description": "",
        "timestamp": "",
        "author": {
            "name": "[HVOLT] WoTB Statistics"},
        "image": {},
        "thumbnail": {},
        "footer": {
            "text": ""},
        "fields": []} 
        
        self.errors = {
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
        'CFE' : '❗ Нераспознанный формат команды'
        }
        
    def return_error_emb(self,error):
        emb_dict = {
        "title": f"Ошибка: {self.error_dict[error]}",
        "color": self.emb_colors['red'],
        "description": self.errors[error],
        "timestamp": "",
        "author": {
          "name": "[HVOLT] WoTB Statistics"},
        "image": {},
        "thumbnail": {'url' : self.error_image},
        "footer": {
          "text": "🔸 Если вы не допускали ошибок,\
          \nобратитесь к разработчику бота"},
        "fields": []}
        err_emb = Embed.from_dict(emb_dict)
        return err_emb
        
    def about_embed(self):
        about = '''🔒 Статус: Альфа тест
🔑 Версия: 0.1.0
📀 Автор: _Zener#1024
```CSS
------UPDATE_LOG-----
ver: 0.0.5 -> 0.1.0
> update WG API
> Add embed messages
> New error messages
> Add region select
```'''
        about_emb = self.empty_embed_dict
        about_emb['title'] = 'Информация о боте'
        about_emb['color'] = 13201920
        about_emb['description'] = about
        about_emb['footer']['text'] = '🔸 Иногда выходят обновления xD'
        embed = Embed.from_dict(about_emb)
        return embed

#m = msg()
#print(m.emb_colors['red'])