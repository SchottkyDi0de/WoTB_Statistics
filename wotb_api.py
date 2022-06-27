import settings
import json
import requests

class App():
    def __init__(self):
        self.application_id = settings.application_id
        self.c_player_name = ''
        self.c_player_id = ''
        self.errors = []
        
        self.battles = 0
        self.winrate = ''
        self.wins = 0
        self.losses = 0
        self.frags = 0
        self.frags8p = 0
        self.shots = 0
        self.hits = 0
        self.accuracy = 0
        self.max_frags = 0
        self.max_xp = 0
        self.survived = 0
        self.survived_and_win = 0
        self.survived_percent = 0
        self.summary_xp = 0
        self.summary_spotted = 0
        self.summary_damage = 0
        self.summary_blocked = 0
 
    def get_id_for_name(self,player_name,return_name = True,region='ru',search_type = 'exact'):
        if len(player_name) < 3:
            self.errors.append('Error: IncorrectPlayerName')
            return 0
        
        req = requests.post(f'https://api.wotblitz.ru/wotb/account/list/?application_id='
        f'{self.application_id}&type={search_type}&search={player_name}&language={region}')
        data = req.content.decode()
        data = json.loads(data)
        
        if data['status'].lower() == 'ok' and data['meta']['count'] == 1:
            account_id = data['data'][0]['account_id']
            self.c_player_id = account_id
            self.c_player_name = data['data'][0]['nickname']
            return account_id
        elif data['status'].lower() == 'error':
            self.errors.append(f'Error {data["error"]["code"]}:{data["error"]["message"]}')
            return 'Error'
        elif data['meta']['count'] > 1:
            self.errors.append('Error: FoundMorePlayers')
            return 'Error'
        elif data['meta']['count'] == 0:
            self.errors.append('Error: PlayerNotFound')
            return 'Error'
            
    def get_player_stat_for_id(self,player_id,region='ru',extra='statistics.rating'):
        req = requests.post(f'https://api.wotblitz.ru/wotb/account/info/?application_id='
        f'{self.application_id}&account_id={player_id}&language={region}&extra={extra}')
        data = req.content.decode()
        data = json.loads(data)
        
        if data['status'].lower() == 'ok' and data['meta']['count'] == 1:
             return data
        elif data['status'].lower() == 'error':
            self.errors.append(f'Error {data["error"]["code"]}:{data["error"]["message"]}')
            return 'Error'
        elif data['meta']['count'] > 1:
            self.errors.append('Error: FoundMorePlayers')
            return 'Error'
        elif data['meta']['count'] == 0:
            self.errors.append('Error: PlayerNotFound')
            return 'Error'
            
    def get_player_stat_for_name(self,player_name,region = 'ru',extra='statistics.rating'):
        player_id = self.get_id_for_name(player_name,region=region)
        data = self.get_player_stat_for_id(player_id,region=region,extra=extra)
        if data == 'Error':
            for i in self.errors:
                print(i)
                return 
        else:
            pass
        
        self.stats_update(data)
        return data

    def stats_update(self,stats):
        data = stats
        #self.c_player_name = data['data'][str(self.c_player_id)]['nickname']
        self.battles = data['data'][str(self.c_player_id)]['statistics']['all']['battles']
        self.winrate = data['data'][str(self.c_player_id)]['statistics']['all']['wins']\
            /self.battles
        self.winrate *= 100 ; self.winrate = round(self.winrate,2)
        self.wins = data['data'][str(self.c_player_id)]['statistics']['all']['wins']
        self.losses = data['data'][str(self.c_player_id)]['statistics']['all']['losses']
        self.frags = data['data'][str(self.c_player_id)]['statistics']['all']['frags']
        self.frags8p = data['data'][str(self.c_player_id)]['statistics']['all']['frags8p']
        self.shots = data['data'][str(self.c_player_id)]['statistics']['all']['shots']
        self.hits = data['data'][str(self.c_player_id)]['statistics']['all']['hits']
        self.accuracy = self.hits/self.shots ; self.accuracy = round(self.accuracy*100,2)
        self.max_frags = data['data'][str(self.c_player_id)]['statistics']['all']['max_frags']
        self.max_xp = data['data'][str(self.c_player_id)]['statistics']['all']['max_xp']
        self.survived = data['data'][str(self.c_player_id)]['statistics']['all']['survived_battles']
        #self.survived_and_win = 1
        self.survived_and_win = data['data'][str(self.c_player_id)]['statistics']['all']['win_and_survived']
        self.survived_percent = self.survived/self.battles ; self.survived_percent = round(self.survived_percent*100,2)
        self.summary_xp = data['data'][str(self.c_player_id)]['statistics']['all']['xp']
        self.summary_spotted = data['data'][str(self.c_player_id)]['statistics']['all']['spotted']
        self.summary_damage = data['data'][str(self.c_player_id)]['statistics']['all']['damage_dealt']
        self.summary_blocked = data['data'][str(self.c_player_id)]['statistics']['all']['damage_received']
        
        self.stats_descriptions = \
f"""```
Игрок: {self.c_player_name}
Количество боёв . . . . {self.battles}
Победы  . . . . . . . . {self.wins}
Поражения . . . . . . . {self.losses}
Процент побед . . . . . {self.winrate}%

Уничтожено техники  . . . . . {self.frags}
Уничтожено техники >= 8 ур  . {self.frags8p}

Выстрелов произведено . . . . {self.shots}
Попаданий по технике врага  . {self.hits}
Точность стрельбы . . . . . . {self.accuracy}%

Максимум уничтожено за бой  . {self.max_frags}
Максимум опыта за бой . . . . {self.max_xp}

Выжил в боях  . . . . . . {self.survived}
Выжил и победил . . . . . {self.survived_and_win}
Процент выживания . . . . {self.survived_percent}%

Всего опыта . . . . . . . . . {self.summary_xp}
Всего урона . . . . . . . . . {self.summary_damage}
Всего заблокированно урона  . {self.summary_blocked}
Всего обнаружено танков . . . {self.summary_spotted}
```"""

        
#app = App()
#data = app.get_player_stat_for_name('_ded_inside__1')
#app.stats_update(data)
#print(app.stats_descriptions)
#print(f'{app.accuracy}%')