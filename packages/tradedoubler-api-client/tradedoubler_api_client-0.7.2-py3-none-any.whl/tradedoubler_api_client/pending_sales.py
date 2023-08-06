import requests
from datetime import datetime, timedelta
import json
from tradedoubler_api_client.utilities import save_list_of_dicts_to_csv, save_dict_to_json


class Pending_Sales:
    def __init__(self, conector):
        self.con = conector

    def __get(self, limit=100, offset=0, start='', end=''):
        req = f'https://connect.tradedoubler.com/advertiser/pendingSales?limit={limit}&offset={offset}'
        if start != '':
            if end == '':
                yesterday = datetime.now()
                yesterdayStr = datetime.strftime(yesterday, '%Y%m%d')
            req = req + f'&startDate={start}&endDate={yesterdayStr}'
        elif end == '':
            yesterday = datetime.now() - timedelta(1)
            yesterdayStr = datetime.strftime(yesterday, '%Y%m%d')
            req = req + f'&endDate={yesterdayStr}'
        else:
            req = req + f'&endDate={end}'

        r = requests.get(req, headers=self.con.get_request_header())
        self.con.handle_errors(r)
        return r.json()

    def get_all(self, start='', end=''):
        """Fetch all pending sales from 'start' to 'end' date in %Y%m%d format. Default for boutth yesterday
        Returns List_Of_Pending_Sales object
         """
        if self.con.print_mode:
            print('\nDownloading pending sales...')
        next_chunk = self.__get(start=start, end=end)
        total = next_chunk['total']
        all_items = next_chunk['items']
        offset = 100
        while total > offset:
            next_chunk = self.__get(offset=offset, start=start, end=end)
            all_items += next_chunk['items']
            offset += 100
        return List_Of_Pending_Sales(all_items, self.con.print_mode)

    def update_sales(self, list_of_items):
        """ make request o Tradedoubler api with list_of_items
        objects in list_of_items must must created by prep_deny or prep_approve methods
        Returns Updated_Sales object
        """
        if self.con.print_mode:
            print(f'\nUpdating {len(list_of_items)} sales...')
        values = {}
        values['items'] = list_of_items
        values = json.dumps(values, indent=4)

        r = requests.put('https://connect.tradedoubler.com/advertiser/pendingSales', data=values, headers=self.con.get_request_header())
        self.con.handle_errors(r)
        return Updated_Sales(r.json(), self.con.print_mode)

    @staticmethod
    def prep_deny(item, reason):
        """ takes item from List_Of_Pending_Sales and reason(int)
        and returns dict with deny transaction response for update_sales method"""
        resp = {}
        resp['transactionId'] = item['transactionId']
        resp['action'] = 'deny'
        resp['reason'] = reason
        return resp

    @staticmethod
    def prep_approve(item):
        """ takes item from List_Of_Pending_Sales and
        returns dict with approve transaction response for update_sales method"""
        resp = {}
        resp['transactionId'] = item['transactionId']
        resp['action'] = 'approve'
        return resp


class List_Of_Pending_Sales:
    def __init__(self, list_of_sales, print_mode):
        self.items = list_of_sales
        self.print_mode = print_mode

    def csv(self, path=''):
        """ save pending sales in csv file in current or in relative 'path' directory"""
        filename = f'all-pending-sales-{datetime.strftime(datetime.now(), "%Y-%m-%d")}.csv'
        save_list_of_dicts_to_csv(self.items, filename, path, self.print_mode)

    def json(self, path=''):
        """ save pending sales in json file in current or in relative 'path' directory"""
        filename = f'all-pending-sales-{datetime.strftime(datetime.now(), "%Y-%m-%d")}.json'
        save_dict_to_json(self.items, filename, path, self.print_mode)

    def get_list_of_ids(self):
        """ returns transactions id as a list of strings """
        list_of_ids = []
        for trans in self.items:
            try:
                list_of_ids.append(str(trans['rxNumber']))
            except ValueError:
                pass
        return list_of_ids


class Updated_Sales:
    def __init__(self, report, print_mode):
        self.total = report['total']
        self.success = report['success']
        self.fail = report['fail']
        self.fails = report['failedItems']
        self.success = report['successfulItems']
        self.print_mode = print_mode

        if self.print_mode:
            print(f'\n{self}')

    def __str__(self):
        return f'Update Results:\nTotal: {self.total}\nSuccess: {self.success}\nFail: {self.fail}'

    # Backward compatibility
    def get_success(self):
        return self.success

    def get_fails(self):
        return self.fails

    def csv(self, status='fail', path=''):
        if status == 'fail':
            filename = f'update-report-fails-{datetime.strftime(datetime.now(), "%Y-%m-%d")}.csv'
            save_list_of_dicts_to_csv(self.fails, filename, path, self.print_mode)
        elif status == 'success':
            filename = f'update-report-successes-{datetime.strftime(datetime.now(), "%Y-%m-%d")}.csv'
            save_list_of_dicts_to_csv(self.success, filename, path, self.print_mode)
        else:
            filename = f'update-report-all-{datetime.strftime(datetime.now(), "%Y-%m-%d")}.csv'
            save_list_of_dicts_to_csv([{"status": '', "transactionId": '', "action": '', "reason": '', "error": ''}] + self.fails + self.success, filename, path, self.print_mode)

    def json(self, status='fail', path=''):
        if status == 'fail':
            filename = f'update-report-fails-{datetime.strftime(datetime.now(), "%Y-%m-%d")}.json'
            save_dict_to_json(self.fails, filename, path, self.print_mode)
        elif status == 'success':
            filename = f'update-report-successes-{datetime.strftime(datetime.now(), "%Y-%m-%d")}.json'
            save_dict_to_json(self.success, filename, path, self.print_mode)
        else:
            filename = f'update-report-all-{datetime.strftime(datetime.now(), "%Y-%m-%d")}.json'
            save_dict_to_json({'total': self.total, 'success': self.success, 'fail': self.fail, 'fails': self.fails, 'successes': self.success}, filename, path, self.print_mode)
