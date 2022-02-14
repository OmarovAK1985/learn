import json

import requests
from tqdm import tqdm
import time
import os


class Yandex_api:
    def __init__(self, token):
        self.token = token

    def __str__(self):
        return self.token

    def create_my_dict(self):
        file = os.path.join(os.getcwd(), 'file_url.json')
        with open(file, mode='r', encoding='utf-8') as dict_file:
            my_dict = json.load(dict_file)
        return my_dict

    def upload_files_from_url(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }
        params = {
            'path': 'vk',
            "templated": False

        }
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources'

        res = requests.put(url=files_url, headers=headers, params=params)

        if res.status_code == 201 or res.status_code == 409:
            for k, v in tqdm(self.create_my_dict().items(), desc='Загрузка файлов на сервер'):
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'OAuth {self.token}'
                }
                params = {
                    'path': f'vk/{v}',
                    'overwrite': False,
                    'disable_redirects': False,
                    'url': k
                }
                files_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'

                requests.post(url=files_url, headers=headers, params=params)
                time.sleep(0.1)
            return 201
        else:
            print('Некорректный Yandex_ID')



