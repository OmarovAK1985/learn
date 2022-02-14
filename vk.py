import json
import os
import requests
from tqdm import tqdm
import time
from datetime import datetime


class VK:
    def __init__(self, user_id):
        self.user_id = user_id

    def __str__(self):
        return self.user_id

    @staticmethod
    def vk_token():
        file = os.path.join(os.getcwd(), 'token.txt')
        with open(file, mode='r', encoding='utf-8') as token_file:
            return token_file.readline()

    def user_get(self):

        url = 'https://api.vk.com/method/users.get'
        params = {
            'access_token': self.vk_token(),
            'v': 5.131,
            'user_ids': self.user_id,
            'fields': 'screen_name',
        }
        res = requests.get(url=url, params=params)
        if len(res.json()['response']) != 0:
            name = res.json()['response'][0]['screen_name']
            id_user = res.json()['response'][0]['id']
            self.photo_get(name=name, id_user=id_user)
            return 1
        else:
            return 0

    def photo_get(self, name, id_user):
        count_photos = int(input("Введите количество фото: "))
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'access_token': self.vk_token(),
            'album_id': 'profile',
            'v': '5.131',
            'extended': 1,
            'owner_id': id_user,
            'count': count_photos
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
            file_extension = None
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
                                    file_extension = i_1['url'].split('.')[-1]
                                    file_extension = file_extension.split('?')[0]
                                    list_sizes.append(val)

                    if k == 'likes':
                        for keys, vals in v.items():
                            if keys == 'count':
                                name_file = f'{vals}.{file_extension}'
                                if name_file in list_name_files:
                                    name_file = f'{vals}_Date_upload_{date}.{file_extension}'
                                list_name_files.append(name_file)
                time.sleep(0.1)
            p = 0
            for i in list_name_files:
                name_file = list_name_files.pop(p)
                list_name_files.insert(p, f'Number_file_{count}_Count_likes_{name_file}')
                p = p + 1
                count = count + 1

            my_dict = dict(zip(list_url, list_name_files))
            list_json = []
            for i, k in zip(list_sizes, list_name_files):
                json_dict = {'file_name': k, 'sizes': i}
                list_json.append(json_dict)

            file = os.path.join(os.getcwd(), 'file.json')
            with open(file=file, mode='w') as file_json:
                json.dump(list_json, file_json, ensure_ascii=False, indent=2)
            if count_photos > len(my_list):
                print(f'Всего фотографий у пользователя с ником {name} - {len(my_list)} шт.')
            if len(my_dict) < len(my_list):
                print(
                    f'Обработано фотографий в количестве {len(my_dict)} шт. Фотографии плохого качества не были обработаны в количестве: {len(my_list) - len(my_dict)} шт.')
            else:
                print(f'Фотографии в количестве {len(my_list)} были успешно обработаны')
            file = os.path.join(os.getcwd(), 'file_url.json')
            with open(file=file, mode='w') as file_json:
                json.dump(my_dict, file_json, ensure_ascii=False, indent=2)

        else:
            print('Не корректный Username')
