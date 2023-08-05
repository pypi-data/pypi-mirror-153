import requests
from datetime import datetime, timedelta
from tradedoubler_api_client.utilities import save_list_of_dicts_to_csv, save_dict_to_json


class Reporting:
    def __init__(self, conector):
        self.con = conector

    def get_transactions(self, status='', fromDate='', toDate='', reportCurrencyCode='PLN', eventId='', **kwargs):
        """ Fetch all transactions. All parameters are optional.

        Params: status ->'P', 'A', 'D' default - all, fromDate, toDate-> %Y%m%d default yesterday , reportCurrencyCode->  iso code default 'PLN', eventId

        Returns Report object with extra methotds
        """
        url = 'https://connect.tradedoubler.com/advertiser/report/transactions/export'
        parameters = f'?format=json&reportCurrencyCode={reportCurrencyCode}'
        if fromDate == '':
            yesterday = datetime.now() - timedelta(8)
            yesterdayStr = datetime.strftime(yesterday, '%Y%m%d')
            parameters += f'&fromDate={yesterdayStr}'
        else:
            parameters += f'&fromDate={fromDate}'
        if toDate == '':
            yesterday = datetime.now() - timedelta(1)
            yesterdayStr = datetime.strfime(yesterday, '%Y%m%d')
            parameters += f'&toDate={yesterdayStr}'
        else:
            parameters += f'&toDate={toDate}'
        if status != '':
            parameters += f'&status={status}'
        if eventId != '':
            parameters += f'&eventId={eventId}'
        for key, value in kwargs.items():
            parameters += f'&{key}={value}'
        r = requests.get(url + parameters,
                         headers=self.con.get_request_header())
        self.con.handle_errors(r)

        return Report(r.json(), fromDate, toDate)


class Report:
    def __init__(self, report, fromDate, toDate):
        self.items = report['items']
        self.currency = report['reportCurrencyCode']
        self.flag = 'all-transactions'
        self.fromDate = fromDate
        self.toDate = toDate

    def filter_sales(self):
        self.items = list(filter(lambda x: x['eventTypeId'] == 5, self.items))
        self.flag = 'sales'

    def filter_leads(self):
        self.items = list(filter(lambda x: x['eventTypeId'] == 4, self.items))
        self.flag = 'leads'

    def csv(self, path=''):
        """ save current state in csv file in current or in relative 'path' directory"""
        filename = f'report-{self.flag}-from-{self.fromDate}-to-{self.toDate}-gen-{datetime.strftime(datetime.now(), "%Y-%m-%d")}.csv'
        save_list_of_dicts_to_csv(self.items, filename, path)

    def json(self, path=''):
        """ save current state in json file in current or in relative 'path' directory"""
        filename = f'report-{self.flag}-from-{self.fromDate}-to-{self.toDate}-gen-{datetime.strftime(datetime.now(), "%Y-%m-%d")}.json'
        save_dict_to_json(self.items, filename, path)
