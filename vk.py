import json
import os
import requests
from tqdm import tqdm
import time
from datetime import datetime
from pprint import pprint


class VK:
    def __init__(self, user_id):
        self.user_id = user_id

    def __str__(self):
        return self.user_id

    def photo_get(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'access_token': '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008',
            'album_id': 'wall',
            'v': '5.131',
            'extended': 1,
            'owner_id': self.user_id,
            'count': 15
        }
        res = requests.get(url=url, params=params)
        count = 0
        for k, v in res.json().items():
            if k == 'response':
                count = 1
        if count == 1:
            my_list = res.json()['response']['items']
            list_url = []
            list_name_files = []
            list_sizes = []
            count = 1
            date = None
            for i in tqdm(my_list, desc='Получение ссылок и присвоение имен файлам'):
                for k, v in i.items():
                    if k == 'date':
                        date = datetime.utcfromtimestamp(v).strftime('%d-%m-%Y')
                    if k == 'sizes':
                        for i_1 in v:
                            for key, val in i_1.items():
                                if val == 'z':
                                    list_url.append(i_1['url'])
                                    list_sizes.append(val)

                    if k == 'likes':
                        for keys, vals in v.items():
                            if keys == 'count':
                                name_file = f'{vals}'
                                count = count + 1
                                if name_file in list_name_files:
                                    name_file = f'{name_file}_Date_upload_{date}'
                                list_name_files.append(name_file)
                time.sleep(0.1)
            my_dict = dict(zip(list_url, list_name_files))
            list_json = []
            for i, k in zip(list_sizes, list_name_files):
                json_dict = {'file_name': k, 'sizes': i}
                list_json.append(json_dict)

            file = os.path.join(os.getcwd(), 'file.json')
            with open(file=file, mode='w') as file_json:
                json.dump(list_json, file_json, ensure_ascii=False, indent=2)
            if len(my_dict) < len(my_list):
                print (f'Обработано фотографий в количестве {len(my_dict)} шт. Фотографии плохого качества не были обработаны в количестве: {len(my_list) - len(my_dict)} шт.')
            else:
                print(f'Фотографии в количестве {len(my_list)} были успешно обработаны')

            return my_dict
        else:
            print('нет прав на фото')
