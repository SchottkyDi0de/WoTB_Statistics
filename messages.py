from discord import Embed

class msg():
    def __init__(self):
        self.empty_embed_dict = {
        "title": "",
        "color": 16711680,
        "description": "",
        "timestamp": "",
        "author": {
        "name": "[HVOLT] WoTB Statistics"
        },
        "image": {},
        "thumbnail": {},
        "footer": {
        "text": ""
        },
        "fields": []
        }
        
        self.errors = {
        'IN' : '❗ Длинна никнейма должна быть хотя бы 3 символа',
        'AE' : '❌ Внутреняя ошибка API ',
        'PNF' : '❌ Игрок с данным именем не найден ',
        'ED' : '❌ Нет данных о данном игроке ',
        'NN' : '❗ Укажите никнейм игрока '
        }
        
    def return_error_emb(self,error):
        emb_dict = {
        "title": "Ошибка!",
        "color": 16711680,
        "description": self.errors[error],
        "timestamp": "",
        "author": {
        "name": "[HVOLT] WoTB Statistics"
        },
        "image": {},
        "thumbnail": {},
        "footer": {
        "text": "🔸 Если ошибка возникла не по вашей вине, \
        \nобратитесь к разработчику бота"
        },
        "fields": []
        }
        err_emb = Embed.from_dict(emb_dict)
        return err_emb
        
    def about_embed(self):
        about = '''🔒 Статус: Альфа тест
🔑 Версия: 0.0.5
📀 Автор: _Zener#1024
```CSS
------UPDATE_LOG-----
ver: 0.0.3 -> 0.0.5
> Server info restyled
> Add Webhook support
> Add new bags
> Remove old bags
```'''
        about_emb = self.empty_embed_dict
        about_emb['title'] = 'Информация о боте'
        about_emb['color'] = 13201920
        about_emb['description'] = about
        about_emb['footer']['text'] = '🔸 Иногда выходят обновления xD'
        embed = Embed.from_dict(about_emb)
        return embed