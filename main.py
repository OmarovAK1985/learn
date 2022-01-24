import vk
from yandex import Yandex_api

count = 0
my_dict = {}
while count == 0:
    id_vk = input('Введите ID пользователя: ')
    vk_id = vk.VK(id_vk)
    my_dict = vk_id.photo_get()
    my_dict_2 = {}
    if type(my_dict) == type(my_dict_2):
        count = 1
count = 0
while count == 0:
    id_yandex = input('Введите ID Yandex: ')
    ya_id = Yandex_api(id_yandex, my_dict)
    my_answer = ya_id.upload_files_from_url()
    if my_answer == 201:
        count = 1






