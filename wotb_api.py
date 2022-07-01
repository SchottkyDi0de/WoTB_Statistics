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
            self.err_code = '400'
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
        =statistics.rating&fields=-statistics.clan&account_id={player_id}')
        json_data = json.loads(data.text)
        return json_data
        
    def player_stats(self,player_name,region = 'ru'):
        player_id = self.player_id(player_name,region=region)
        stats = self.player_stats_for_id(player_id,region=region)
        #print(stats)
        return stats
        
        
        
#api = get()
#ps = parser.pars()
#stat = api.player_stats('_ded_inside__1')
#print(dict.keys(stat['data']))
#print(ps.get_data(stat,id))