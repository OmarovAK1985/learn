import requests
from tqdm import tqdm
import time


class Yandex_api:
    def __init__(self, token, my_dict):
        self.token = token
        self.my_dict = my_dict

    def __str__(self):
        return self.token

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
            for k, v in tqdm(self.my_dict.items(), desc='Загрузка файлов на сервер'):
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'OAuth {self.token}'
                }
                params = {
                    'path': f'vk/{k}',
                    'overwrite': False,
                    'disable_redirects': True,
                    'url': v
                }
                files_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'

                requests.post(url=files_url, headers=headers, params=params)
                time.sleep(0.1)
            return 201
        else:
            print('Некорректный Yandex_ID')



