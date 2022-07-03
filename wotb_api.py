import settings
import json
import requests
import parser

#400 - name < 3
#401 - api_error
#402 - player_not_found
#403 - empty_data

class get():
    
    def __init__(self):
        self.__app_id = settings.WG_APP_ID
        self.err_code = ''
        self.last_name = ''
        self.last_id = ''
        self.error_list = [
        'IN','AE','PNF','ED']
    
    def player_id(self,player_name,region = 'ru',search_type = 'exact'):
        if len(player_name) < 3:
            self.err_code = 'IN'
            print('Error: IN')
            return 'IN'

        data = requests.post(f'https://api.wotblitz.ru/wotb/account/list/\
        ?application_id={self.__app_id}&search={player_name}\
        &language={region}&type={search_type}')
        print(f'Request: {player_name}')
        json_data = json.loads(data.text)
        #print(json_data)
        print('Result:')
        if json_data['status'] == 'error':
            print('Error: AE')
            return 'AE'
        elif json_data['meta']['count'] == 0:
            print('Error: PNF')
            return 'PNF'
        elif json_data['data'] == []:
            print('Error: ED')
            return 'ED'
        else:
            print(f'''  staus: {json_data["status"]}
  meta:
    count: {json_data["meta"]["count"]}
  data:
    current ID: {json_data["data"][0]["account_id"]}
    current nickname: {json_data["data"][0]["nickname"]}\n''')
            self.last_name = json_data['data'][0]['nickname']
            self.last_id = json_data['data'][0]['account_id']
            return self.last_id
            
    def error_pass(self,data):
        for i in self.error_list:
            if data == i:
                self.err_code = i
                return True
        return False
        self.err_code = ''

    def player_stats_for_id(self,player_id,region = 'ru',rating_stats = False):
        #print(self.error_pass(player_id))
        if self.error_pass(player_id):
            return self.err_code
        else:
            pass
        
        if rating_stats:
            extra = 'statistics.rating'
        else:
            extra = ''
            
        data = requests.post(f'https://api.wotblitz.ru/wotb/account/info/\
        ?application_id={self.__app_id}&language={region}&extra\
        ={extra}&fields=-statistics.clan&account_id={player_id}')
        json_data = json.loads(data.text)
        return json_data
        
    def player_stats(self,player_name,region = 'ru'):
        player_id = self.player_id(player_name,region=region)
        stats = self.player_stats_for_id(player_id,region=region)
        #print(stats)
        return stats
    
    def server_status(self):
        data = requests.post(f'https://api.worldoftanks.ru/wgn/servers/\
info/?application_id={settings.WG_APP_ID}&game=wotb')
        json_data = json.loads(data.text)
        #print(json_data)
        
        if json_data['status'] == 'ok':
            return json_data
        else:
            self.err_code = 'AE'
            return 'AE'
        
        
        
#api = get()
#ps = parser.pars()
#api.player_stats('jasz777','ru')
#data = api.server_status()
#print(ps.server_status(data))