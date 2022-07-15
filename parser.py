import datetime as dt
from discord import Embed

class pars():
    def __init__(self):
        self.dt = dt
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
        self._region_list = [
        'ru','eu',
        'na','asia',
        ]
        self.color_gradient = [
        11321088,
        12545024,
        12533760,
        16711680,
        65280,
        ]
        
        self.__emb_dict = {
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

    def region_time(self,region):
        region = region.lower()
        if region == 'ru':
            offset = dt.timedelta(hours=3)
            tz_msc = dt.timezone(offset, name='| MSC (UTC + 3)')
            tm = dt.datetime.now(tz=tz_msc).strftime("%H:%M")
            tm += ' ' + tz_msc.tzname(dt.datetime.now())
            return tm
        elif region == 'eu':
            offset = dt.timedelta(hours=1)
            tz_cet = dt.timezone(offset, name='| CET (UTC + 1)')
            tm = dt.datetime.now(tz=tz_cet).strftime("%H:%M")
            tm += ' ' + tz_cet.tzname(dt.datetime.now())
            return tm
        elif region == 'na':
            offset = dt.timedelta(hours=-4)
            tz_edt = dt.timezone(offset, name='| EDT (UTC -4)')
            tm = dt.datetime.now(tz=tz_edt).strftime("%H:%M")
            tm += ' ' + tz_edt.tzname(dt.datetime.now())
            return tm
        elif region == 'asia':
            offset = dt.timedelta(hours=9)
            tz_kst = dt.timezone(offset, name='| KST (UTC +9)')
            tm = dt.datetime.now(tz=tz_kst).strftime("%H:%M")
            tm += ' ' + tz_kst.tzname(dt.datetime.now())
            return tm
            
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
        description = f'''
🖥️ Сервер: **{server_name}**
🕓 Время региона: **{self.region_time(server_name)}**
🎯 Игроков онлайн: **{players_online:,}**
🖍️ Статус: **{'ONLINE  🟢' if players_online > 0 else 'OFFLINE 🔴'}**
'''     
        emb_dict = self.__emb_dict
        emb_dict['title'] = 'Статус серверов WoT Blitz'
        emb_dict['color'] = self.color_set_online(players_online)
        emb_dict['description'] = description
        emb_dict['footer']['text'] = '🔸 Цвет рамки текста зависит от текущего онлайна'
        #print(multi_server_status)
        embed = Embed.from_dict(emb_dict)
        return embed


    def server_status_all(self,data):
        multi_description = []
        multi_description.clear()
        alive_counter = 0
        for i in range(4):
            players_online = data[i]['data']['wotb'][0]['players_online']
            
            if players_online > 0:
                status = ('ONLINE  🟢')
                alive_counter += 1
            else:
                status = ('OFFLINE 🔴')
                alive_counter += 0
                
            server_name = data[i]['data']['wotb'][0]['server']
            multi_description.append(f'''
🖥️ Сервер: **{server_name}**
🕓 Время региона: {self.region_time(server_name)}
🎯 Игроков онлайн: **{players_online:,}**
🖍️ Статус: **{status}**
🔸🔸🔸🔸🔸🔸🔸🔸🔸🔸🔸🔸🔸🔸''')
        emb_dict = self.__emb_dict
        emb_dict['title'] = 'Статус серверов WoT Blitz'
        emb_dict['color'] = self.color_gradient[alive_counter]
        emb_dict['description'] = ''
        for i in range(4):
            emb_dict['description'] += multi_description[i]
            
        emb_dict['footer']['text'] = '🔸 Цвет рамки текста зависит от количества \
                                                                активных серверов'
        #print(multi_server_status)
        embed = Embed.from_dict(emb_dict)
        return embed
        
    def get_data(self,data,p_id):
        p_id = str(p_id)
        d = data
        
        # stats_variables:
            
        # common:
        nickname = d['data'][p_id]['nickname']
        created_at = self.dt.datetime.fromtimestamp(d['data'][p_id]['created_at'])
        datetime_now = self.dt.datetime.now()
        account_age = datetime_now - created_at ; account_age = account_age.days
        last_battle = self.dt.datetime.fromtimestamp(d['data'][p_id]['last_battle_time'])
        updated_at = self.dt.date.fromtimestamp(d['data'][p_id]['updated_at'])
        
        # battle_stats:
        spotted = d['data'][p_id]['statistics']['all']['spotted']
        hits = d['data'][p_id]['statistics']['all']['hits']
        frags = d['data'][p_id]['statistics']['all']['frags']
        max_xp = d['data'][p_id]['statistics']['all']['max_xp']
        wins = d['data'][p_id]['statistics']['all']['wins']
        losses = d['data'][p_id]['statistics']['all']['losses']
        capture_points = d['data'][p_id]['statistics']['all']['capture_points']
        battles = d['data'][p_id]['statistics']['all']['battles']
        damage_dealt = d['data'][p_id]['statistics']['all']['damage_dealt']
        damage_received = d['data'][p_id]['statistics']['all']['damage_received']
        max_frags = d['data'][p_id]['statistics']['all']['max_frags']
        shots = d['data'][p_id]['statistics']['all']['shots']
        frags8p = d['data'][p_id]['statistics']['all']['frags8p']
        xp = d['data'][p_id]['statistics']['all']['xp']
        win_and_survived = d['data'][p_id]['statistics']['all']['win_and_survived']
        survived_battles = d['data'][p_id]['statistics']['all']['survived_battles']
        dropped_capture_point = d['data'][p_id]['statistics']['all']['dropped_capture_points']
        
        # custom_stats
        if battles == 0:
            winrate = 0
            accuracy = 0
            survival = 0
            rd_damage = 0
            fr8_fr = 0
            #capture_points_coeff = 0
            awg_damage = 0
        else:
            winrate = round((wins / battles)*100,2)
            accuracy = round((hits / shots)*100,2)
            survival = round((survived_battles / battles)*100,2)
            rd_damage = round((damage_dealt / damage_received),2)
            fr8_fr = round((frags8p / (frags-frags8p)),2)
            #capture_points_coeff = round((capture_points/dropped_capture_point),2)
            awg_damage = damage_dealt // battles
            
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
╠|Средний урон:  {awg_damage:,}
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

