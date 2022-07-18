'''
This module is designed to generate "embed" objects,
which are then passed to main.by
'''
import datetime as date
from discord import Embed

class Generate():
    '''
    Класс для сборки различных 'embed' объектов.
    Содержит также вспомогательные методы.
    '''
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
        self._region_list = [
        'ru','eu',
        'na','asia',
        ]
        self.color_gradient = [
        11321088, 12533760,
        12545024, 16711680,
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
        offset = date.timedelta(hours=3)
        self.tz_msc = date.timezone(offset, name='| MSC (UTC + 3)')
        offset = date.timedelta(hours=1)
        self.tz_cet = date.timezone(offset, name='| CET (UTC + 1)')
        offset = date.timedelta(hours=-4)
        self.tz_edt = date.timezone(offset, name='| EDT (UTC -4)')
        offset = date.timedelta(hours=9)
        self.tz_kst = date.timezone(offset, name='| KST (UTC +9)')

    def color_set_online(self, online):
        '''
        Возврашает определённое число в зависимости от онлайна
        на сервере. Это число характерещует цвет рамки в embed
        сообщениях
        '''
        color = 000000
        if online < 8000:
            color = self.color_list['red']
        elif online < 15000:
            color = self.color_list['orange']
        elif online >= 15000:
            color = self.color_list['green']
        return color

    def region_time(self,region):
        '''
        Определение времени для разных часовых поясов.
        Используется в get_server_status
        '''
        region = region.lower()
        if region == 'ru':
            time = date.datetime.now(tz=self.tz_msc).strftime("%H:%M")
            time += ' ' + self.tz_msc.tzname(date.datetime.now())
            return time

        if region == 'eu':
            time = date.datetime.now(tz=self.tz_cet).strftime("%H:%M")
            time += ' ' + self.tz_cet.tzname(date.datetime.now())
            return time

        if region == 'na':
            time = date.datetime.now(tz=self.tz_edt).strftime("%H:%M")
            time += ' ' + self.tz_edt.tzname(date.datetime.now())
            return time

        if region == 'asia':
            time = date.datetime.now(tz=self.tz_kst).strftime("%H:%M")
            time += ' ' + self.tz_kst.tzname(date.datetime.now())
            return time
        return None

    def color_set_winrate(self, winrate):
        '''
        Установка цвета в зависимости от % побед
        указанного аккаунта. Принимает 1 значение
        % побед. Возвращает специальное число,
        которое задаёт цвет для будущего сообщения
        '''
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
        '''
        Этот метод генерирует нам embed объект со списком
        статусов одного сервера wot_blitz
        '''
        players_online = data['data']['wotb'][0]['players_online']
        server_name = data['data']['wotb'][0]['server']
        description = f'''
🖥️ Сервер: **{server_name}**
🕓 Время региона: **{self.region_time(server_name)}**
🎯 Игроков онлайн: **{players_online:,}**
🖍️ Статус: **{'ONLINE  🟢' if players_online > 0 else 'OFFLINE  🔴'}**
'''
        emb_dict = self.__emb_dict
        emb_dict['footer']['text'] = '🔸 Цвет рамки текста зависит от текущего онлайна'
        emb_dict['color'] = self.color_set_online(players_online)
        emb_dict['title'] = 'Статус серверов WoT Blitz'
        emb_dict['description'] = description
        embed = Embed.from_dict(emb_dict)
        return embed

    def server_status_all(self,data):
        '''
        Этот метод генерирует нам embed объект со списком
        статусов всех серверов wot_blitz
        '''
        multi_description = []
        multi_description.clear()
        alive_counter = 0
        # alive_counter - переменная, в которой хранится число 'живых' серверов
        for i in range(4):
            players_online = data[i]['data']['wotb'][0]['players_online']
            server_name = data[i]['data']['wotb'][0]['server']
            multi_description.append(f'''
🖥️ Сервер: **{server_name}**
🕓 Время региона: {self.region_time(server_name)}
🎯 Игроков онлайн: **{players_online:,}**
🖍️ Статус: **{'ONLINE  🟢' if players_online > 0 else 'OFFLINE  🔴'}**
🔸🔸🔸🔸🔸🔸🔸🔸🔸🔸🔸🔸🔸🔸''')
        emb_dict = self.__emb_dict
        emb_dict['title'] = 'Статус серверов WoT Blitz'
        emb_dict['color'] = self.color_gradient[alive_counter]
        emb_dict['description'] = ''
        for i in range(4):
            emb_dict['description'] += multi_description[i]

        emb_dict['footer']['text'] = '🔸 Цвет рамки текста зависит от количества \
                                      активных серверов'
        embed = Embed.from_dict(emb_dict)
        return embed

    def account_data(self,data,player_id):
        """
        Этот метод генерирует нам embed объект со
        статистикой игрока.
        Переменная "data" сокращена до "d" в угоду
        длинны строк. Тоже касается и "player_id"
        """
        p_id = str(player_id)
        d = data
        battles = d['data'][p_id]['statistics']['all']['battles']
        
        # переменная battles задаётся заранее, это необходимо 
        # для некоторых расчётов
        

        # общие данные аккаунта:
        if battles == 0:
            last_battle = '\'Нет данных\''
        else:
            last_battle = date.datetime.fromtimestamp(d['data'][p_id]['last_battle_time'])

        created_at = date.datetime.fromtimestamp(d['data'][p_id]['created_at'])
        updated_at = date.datetime.fromtimestamp(d['data'][p_id]['updated_at'])
        nickname = d['data'][p_id]['nickname']

        datetime_now = date.datetime.now()
        account_age = datetime_now - created_at
        account_age = account_age.days

        # боевая статистика:
        dropped_capture_point = d['data'][p_id]['statistics']['all']['dropped_capture_points']
        win_and_survived = d['data'][p_id]['statistics']['all']['win_and_survived']
        survived_battles = d['data'][p_id]['statistics']['all']['survived_battles']
        damage_received = d['data'][p_id]['statistics']['all']['damage_received']
        capture_points = d['data'][p_id]['statistics']['all']['capture_points']
        damage_dealt = d['data'][p_id]['statistics']['all']['damage_dealt']
        spotted = d['data'][p_id]['statistics']['all']['spotted']
        max_xp = d['data'][p_id]['statistics']['all']['max_xp']
        frags = d['data'][p_id]['statistics']['all']['frags']
        hits = d['data'][p_id]['statistics']['all']['hits']

        losses = d['data'][p_id]['statistics']['all']['losses']
        wins = d['data'][p_id]['statistics']['all']['wins']

        max_frags = d['data'][p_id]['statistics']['all']['max_frags']
        frags8p = d['data'][p_id]['statistics']['all']['frags8p']
        shots = d['data'][p_id]['statistics']['all']['shots']
        xp = d['data'][p_id]['statistics']['all']['xp']

        # создание дополнительных статистик
        if battles == 0:
            frags8p_coeff = 0
            awg_damage = 0
            rd_damage = 0
            survival = 0
            accuracy = 0
            winrate = 0
            battles_per_day = 0
        else:
            battles_per_day = battles // account_age
            if battles_per_day == 0:
                battles_per_day = '< 1'

            rd_damage = round((damage_dealt / damage_received),2)
            frags8p_coeff = round((frags8p / (frags-frags8p)),2)
            survival = round((survived_battles / battles)*100,2)
            winrate = round((wins / battles)*100,2)
            accuracy = round((hits / shots)*100,2)
            awg_damage = damage_dealt // battles

        # текст, который будет помещён в embed
        self.last_data = f'''```python
╔|Информация обновлена:
╚|[{updated_at.strftime("%Y|%m|%d - %H:%M")}]
--------|Основная информация|--------
╔|Аккаунт создан: [{created_at.strftime("%Y|%m|%d - %H:%M")}]
╠|Последный бой: [{last_battle.strftime("%Y|%m|%d - %H:%M")}]
╠|ID Аккаунта: {p_id}
╠|Возраст аккаунта: {account_age} дней.
╚|Боёв в сутки: {battles_per_day}
---------|Боевая статистика|---------
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
╚|Коэффициент frags8p:  {frags8p_coeff}

╔|Очки захвата:  {capture_points:,}
╚|Сбитые очки захвата:  {dropped_capture_point:,}

╔|Всего опыта:  {xp:,}
╚|Максимум опыта за бой:  {max_xp:,}

╔|Максимум уничтожено за бой:  {max_frags:,}
╚|Техники обнаруженно:  {spotted:,}
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
