'''
Модуль для работы с
Wargaming API
'''
import json
import requests
import settings


class API():
    '''
    Главный класс API
    В нём выполняются все запросы к WG API
    '''
    def __init__(self):
        self.last_error = ''
        self.last_id = ''
        self.__app_id = settings.WG_APP_ID
        self.region_reset = False
        # список регионов
        self.regions_list = [
        'ru',
        'eu',
        'com',
        'asia']
        # лист из ошибок
        self.error_list = [
        'PNF', 'SNS',
        'FMP', 'ND',
        'IN', 'IS',
        'AE', 'NN',]
        # расшифровка ошибок
        self.error_dict = {
        'PNF' : 'PLAYER_NOT_FOUND',
        'IN' : 'INCORRECT_NAME',
        'IS' : 'INCORRECT_SEARCH',
        'SNS' : 'SEARCH_NOT_SPECIFIED',
        'ND' : 'NO_DATA',
        'NN' : 'NO_NAME'}
        '''
        Все эти списки ошибок нужны для того, чтобы их
        можно было обрабатывать. Методы данного класа могут
        вернуть результат или код ошибки ('например nn')
        '''

    def region_handler(self,region):
        '''
        Обработка региона. Если регион указан не верно
        то этот метод возвращает значени по умолчанию,
        также переводит флаг self.region_reset в значение True
        '''
        region = region.lower()

        if region == 'ru':
            self.region_reset = False
            return 'ru'

        if region == 'eu':
            self.region_reset = False
            return 'eu'

        if region == 'na':
            self.region_reset = False
            return 'com'

        if region == 'asia':
            self.region_reset = False
            return 'asia'

        self.region_reset = True
        return 'ru'

    def error_finder(self,data,err_type = 'ID'):
        '''
        Метод поиск ошибок. если ошибка найдена, то возвращаем её имя.
        Так как метод применяется для обработки разных данных
        то тип данных, с которыми методу предстоит работать указывается
        в параметре err_type
        'ID' (по умолчанию) - Данные, которые API возвращает в методе
                              player_id
        'PD' - Данные, которые возвращает метод get_player_stats_id

        Если не указывать тип данных, то будут искаться ошибки - свойственные
        всем типам ответа.
        '''
        self.last_error = ''
        if data['status'] == 'error':
            if data['error']['message'] == 'INVALID_SEARCH':
                self.last_error = 'IS'
                return self.last_error

            if data['error']['message'] == 'SEARCH_NOT_SPECIFIED':
                self.last_error = 'SNS'
                return self.last_error

            self.last_error = 'AE'
            return self.last_error

        if err_type == 'ID':
            if data['meta']['count'] == 0:
                self.last_error = 'PNF'
                return self.last_error

            if data['meta']['count'] > 1:
                self.last_error = 'FMP'
                return self.last_error

        if err_type == 'PD':
            if data['data'][str(self.last_id)] is None:
                self.last_error = 'ND'
                return self.last_error

        self.last_error = ''
        return data

    def error_pass(self,data):
        '''
        Проверка на наличие ошибок
        '''
        for i in self.error_list:
            if data == i:
                self.last_error = i
                return True

        self.last_error = ''
        return False

    def nickname_handler(self,nickname):
        '''
        Проверка корректности никнема
        '''
        if len(nickname) < 3:
            self.last_error = 'IN'
        elif len(nickname) > 24:
            self.last_error = 'IN'

    def get_player_id(self,nickname,region='ru'):
        '''
        Получение ID игрока по никнейму
        '''
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

        self.last_id = j_data['data'][0]['account_id']
        return self.last_id

    def get_player_stats_id(self,account_id,region = 'ru'):
        '''
        Получение игровой статистики по ID
        '''
        region = self.region_handler(region)
        data = requests.post(f'https://api.wotblitz.{region}/wotb/account/info/\
        ?application_id={self.__app_id}\
        &fields=-statistics.clan&account_id={account_id}')
        j_data = json.loads(data.text)
        self.error_finder(j_data,'PD')
        if self.last_error != '':
            return self.last_error

        return j_data

    def get_player_stats(self,nickname,region='ru'):
        '''
        Метод для получения игровой статистики по никнейму
        использует методы:
        account_id и get_player_stats_id
        '''
        self.last_error = ''
        account_id = self.get_player_id(nickname,region)
        if self.last_error != '':
            return self.last_error

        stats = self.get_player_stats_id(account_id,region)
        return stats

    def get_server_status(self,server = 'ru'):
        '''
        Получаем статус сервера. сервер указывается параметром
        'server' по умолчанию это ru сервер
        Если server == 'all' то возвращаем списо с данными всхе
        серверов (работает медленно)
        '''
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

                input_data.append(sm_data)

            return input_data

        server = self.region_handler(server)
        s_data = requests.post(f'https://api.worldoftanks.{server}\
/wgn/servers/info/?application_id={self.__app_id}&game=wotb')
        s_data = json.loads(s_data.text)
        self.error_finder(s_data,'')
        if self.last_error != '':
            return self.last_error

        return s_data

if __name__ == '__main__':
    # Данная конструкция сделанна для тестирования
    pass
