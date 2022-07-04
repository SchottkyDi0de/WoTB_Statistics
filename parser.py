import datetime as dt
from discord import Embed

class pars():
    def __init__(self):
        self.last_data = ''
        self.last_server_status = ''
        self.color_list = {
        'gray' : 12237498,
        'green' : 65280,
        'blue' : 2518253,
        'purple' : 12464383,
        'red' : 16711680,
        'orange' : 15763456,
        }
        
        self.emb_dict = {
        "title": '',
        "color": '',
        "description": '',
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
        
    def color_set_online(self, online):
        color = 000000
        if online < 8000:
            color = self.color_list['red']
        elif online < 15000:
            color = self.color_list['orange']
        elif online >= 15000:
            color = self.color_list['green']
        return color
            
    def color_set_winrate(self, winrate):
        color = 000000
        if winrate < 48:
            color = self.color_list['gray']
        elif winrate < 60:
            color = self.color_list['green']
        elif winrate < 70:
            color = self.color_list['blue']
        elif winrate >= 70:
            color = self.color_list['purple']
        return color
        
    def server_status(self,data):
        players_online = data['data']['wotb'][0]['players_online']
        server_name = data['data']['wotb'][0]['server']
        self.last_server_status = f'''
🖥️ Сервер: {server_name}
🎯 Игроков онлайн: {players_online:,}
🖍️ Статус: ONLINE
'''
        emb_dict = self.emb_dict
        emb_dict['title'] = 'Статус серверов WoT Blitz'
        emb_dict['color'] = self.color_set_online(players_online)
        emb_dict['description'] = self.last_server_status
        emb_dict['footer']['text'] = '🔸 Цвет рамки текста зависит от текущего онлайна'
        embed = Embed.from_dict(emb_dict)
        return embed
        
    def get_data(self,data,id):
        id = str(id)
        d = data
        
        # stats_variables:
            
        # common:
        nickname = d['data'][id]['nickname']
        created_at = dt.datetime.fromtimestamp(d['data'][id]['created_at'])
        datetime_now = dt.datetime.now()
        account_age = datetime_now - created_at ; account_age = account_age.days
        last_battle = dt.datetime.fromtimestamp(d['data'][id]['last_battle_time'])
        updated_at = dt.date.fromtimestamp(d['data'][id]['updated_at'])
        
        # battle_stats:
        spotted = d['data'][id]['statistics']['all']['spotted']
        hits = d['data'][id]['statistics']['all']['hits']
        frags = d['data'][id]['statistics']['all']['frags']
        max_xp = d['data'][id]['statistics']['all']['max_xp']
        wins = d['data'][id]['statistics']['all']['wins']
        losses = d['data'][id]['statistics']['all']['losses']
        capture_points = d['data'][id]['statistics']['all']['capture_points']
        battles = d['data'][id]['statistics']['all']['battles']
        damage_dealt = d['data'][id]['statistics']['all']['damage_dealt']
        damage_received = d['data'][id]['statistics']['all']['damage_received']
        max_frags = d['data'][id]['statistics']['all']['max_frags']
        shots = d['data'][id]['statistics']['all']['shots']
        frags8p = d['data'][id]['statistics']['all']['frags8p']
        xp = d['data'][id]['statistics']['all']['xp']
        win_and_survived = d['data'][id]['statistics']['all']['win_and_survived']
        survived_battles = d['data'][id]['statistics']['all']['survived_battles']
        dropped_capture_point = d['data'][id]['statistics']['all']['dropped_capture_points']
        
        # custom_stats
        if battles == 0:
            winrate = 0
            accuracy = 0
            survival = 0
            rd_damage = 0
            fr8_fr = 0
            capture_points_coeff = 0
        else:
            winrate = round((wins / battles)*100,2)
            accuracy = round((hits / shots)*100,2)
            survival = round((survived_battles / battles)*100,2)
            rd_damage = round((damage_dealt / damage_received),2)
            fr8_fr = round((frags8p / (frags-frags8p)),2)
            capture_points_coeff = round((capture_points/dropped_capture_point),2)
            
        # text:
        self.last_data = f'''```
--------|Основная информация|------
╔|Аккаунт создан: {created_at}
╠|ID Аккаунта: {id}
╠|Последный бой: {last_battle}
╠|Информация обновлена: {updated_at}
╚|Возраст аккаунта: {account_age} дней.
---------|Боевая статистика|--------
╔|Боёв сыграно: {battles:,}
╠|Победы:  {wins:,}
╠|Поражения:  {losses:,}
╚|Процент побед:  {winrate}%

╔|Выстрелы:  {shots:,}
╠|Попадания:  {hits:,}
╚|Точность стрельбы:  {accuracy}%

╔|Выжил в боях:  {survived_battles:,}
╠|Победил и выжил:  {win_and_survived:,}
╚|Процент выживания:  {survival}%

╔|Нанесено урона:  {damage_dealt:,}
╠|Получено урона:  {damage_received:,}
╚|Соотношение урона  (н/п): {rd_damage}

╔|Уничтожено танков:  {frags:,}
╠|Уничтожено танков >= 8 ур:  {frags8p:,}
╚|Клэффициент frags8p:  {fr8_fr}

╔|Очки захвата:  {capture_points:,}
╚|Сбитые очки захвата:  {dropped_capture_point:,}

╔|Всего опыта:  {xp:,}
╚|Максимум опыта за бой:  {max_xp:,}

═|Максимум уничтожено за бой:  {max_frags:,}
```'''
        emb_dict_stats = {
        "title": nickname,
        "color": self.color_set_winrate(winrate),
        "description": self.last_data,
        "timestamp": "",
        "author": {
        "name": "[HVOLT] WoTB Statistics"
        },
        "image": {},
        "thumbnail": {},
        "footer": {
        "text": "🔸 Цвет рамки сообщения зависит от % побед исследуемого аккаунта."
        },
        "fields": []
        }
        embed_stats = Embed.from_dict(emb_dict_stats)
      
        return embed_stats