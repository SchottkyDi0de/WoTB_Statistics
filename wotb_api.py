import json
import requests
import settings


class API():
    def __init__(self):
        # инициализируем переменные
        # которые пригодятся в будущем.
        self.last_error = ''
        self.last_stats = ''
        self.last_server_info = ''
        self.last_region = ''
        self.last_id = ''
        self.__app_id = settings.WG_APP_ID
        self.region_reset = False
        self.regions_list = [
        'ru',
        'eu',
        'com',
        'asia'              ]
        self.error_list = [
        'PNF', 
        'SNS',
        'FMP', 
        'ND',
        'IN',
        'IS',
        'AE',
        'NN',       ]
        self.error_dict = {
        'PNF' : 'PLAYER_NOT_FOUND',
        'IN' : 'INCORRECT_NAME',
        'IS' : 'INCORRECT_SEARCH',
        'SNS' : 'SEARCH_NOT_SPECIFIED',
        'ND' : 'NO_DATA',
        'NN' : 'NO_NAME'
        }
        # BR - BAD REGION          # IN - INCORRECT NAME
        # PNF - PLAYER NOT FOUND   # IS - INCORRECT SEARCH
        # FMP - FOUND MORE PLAYERS # SNS - SEARCH NOT SPECIFIED
        # ND - NO DATA
        
    def region_handler(self,region):
        region = region.lower()
        if region == 'ru':
            self.region_reset = False
            return 'ru'
        elif region == 'eu':
            self.region_reset = False
            return 'eu'
        elif region == 'na':
            self.region_reset = False
            return 'com'
        elif region == 'asia':
            self.region_reset = False
            return 'asia'
        
        self.region_reset = True
        return 'ru'

    def error_finder(self,data,err_type = 'ID'):
        # ищем ошибки, если они есть,
        # то возвращаем её имя
        self.last_error = ''
        if data['status'] == 'error':
            if data['error']['message'] == 'INVALID_SEARCH':
                self.last_error = 'IS'
                return self.last_error
            elif data['error']['message'] == 'SEARCH_NOT_SPECIFIED':
                self.last_error = 'SNS'
                return self.last_error
            else:
                self.last_error = 'AE'
                return self.last_error
        
        if err_type == 'ID':
            if data['meta']['count'] == 0:
                self.last_error = 'PNF'
                return self.last_error
            elif data['meta']['count'] > 1:
                self.last_error = 'FMP'
                return self.last_error
            
        if err_type == 'PD':
            if data['data'][str(self.last_id)] == None:
                self.last_error = 'ND'
                return self.last_error
                
        self.last_error = ''
        return data

    def error_pass(self,data):
        for i in self.error_list:
            if data == i:
                self.last_error = i
                return True
        self.last_error = ''
        return False
        
    def nickname_handler(self,nickname):
        if len(nickname) < 3:
            self.last_error = 'IN'
        elif len(nickname) > 24:
            self.last_error = 'IN'
        
    def get_player_id(self,nickname,region='ru'):
        self.last_id = ''
        self.nickname_handler(nickname)
        region = self.region_handler(region)
        if self.last_error != '':
            return self.last_error
            
        data = requests.post(f'https://api.wotblitz.{region}/wotb/account/list/\
        ?application_id={self.__app_id}&search={nickname}&type=exact')
        j_data = json.loads(data.text)
        self.error_finder(j_data,'ID')
        if self.last_error != '':
            self.last_id = None
            return self.last_error
        else:
            self.last_id = j_data['data'][0]['account_id']
            return self.last_id

    def get_player_stats_id(self,account_id,region = 'ru'):
        region = self.region_handler(region)
        data = requests.post(f'https://api.wotblitz.{region}/wotb/account/info/\
        ?application_id={self.__app_id}\
        &fields=-statistics.clan&account_id={account_id}')
        j_data = json.loads(data.text)
        self.error_finder(j_data,'PD')
        if self.last_error != '':
            return self.last_error
        else:
            return j_data
            
    def get_player_stats(self,nickname,region='ru'):
        self.last_error = ''
        account_id = self.get_player_id(nickname,region)
        if self.last_error != '':
            return self.last_error
        stats = self.get_player_stats_id(account_id,region)
        return stats

    def get_server_status(self,server = ''):
        if server.lower() == 'all':
            input_data = []
            sm_data = ''
            
            for i in self.regions_list:
                sm_data = requests.post(f'https://api.worldoftanks.{i}\
/wgn/servers/info/?application_id={self.__app_id}&game=wotb')
                sm_data = json.loads(sm_data.text)
                self.error_finder(sm_data,'')
                if self.last_error != '':
                    return self.last_error
                else:
                    input_data.append(sm_data)
                    
            return input_data
            
        server = self.region_handler(server)
        s_data = requests.post(f'https://api.worldoftanks.{server}\
/wgn/servers/info/?application_id={self.__app_id}&game=wotb')
        s_data = json.loads(s_data.text)
        self.error_finder(s_data,'')
        if self.last_error != '':
            return self.last_error
        else:
            return s_data

if __name__ == '__main__':
    
    a = API()
    dat = a.get_server_status(server='ru')    
    print(dat)
    dat = a.get_server_status(server='all')    
    #print(dat)