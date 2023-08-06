import sys
import os
import csv
import json


def file_colision_detector(file_name, extra_path):
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    file_name = file_name.split('.')

    if extra_path != '':
        path = f'{path}/{extra_path}'
        if not os.path.isdir(f'{path}/'):
            os.mkdir(path)

    if os.path.isfile(f'{path}/{file_name[0]}-(0).{file_name[1]}'):
        i = 1
        while os.path.isfile(f'{path}/{file_name[0]}-({i}).{file_name[1]}'):
            i += 1
        return f'{path}/{file_name[0]}-({i}).{file_name[1]}'
    else:
        return f'{path}/{file_name[0]}-(0).{file_name[1]}'


def save_list_of_dicts_to_csv(list_of_dicts, filename, path, print_mode):
    if len(list_of_dicts) == 0:
        if print_mode:
            print('\nnothing to save in csv\n')
        return False
    filename = file_colision_detector(filename, path)
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        wr = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        wr.writerow(list(list_of_dicts[0].keys()))

        for item in list_of_dicts:
            # remove empty lines
            if all([x == '' for x in list(item.values())]):
                continue
            wr.writerow(list(item.values()))

    if print_mode:
        print(f'\nFile is ready: {filename}\n')


def save_dict_to_json(dct, filename, path, print_mode):
    filename = file_colision_detector(filename, path)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(dct, f, ensure_ascii=False, indent=4)

    if print_mode:
        print(f'\nFile is ready: {filename}\n')
