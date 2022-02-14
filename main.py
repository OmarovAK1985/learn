import vk
from yandex import Yandex_api

if __name__ == "__main__":
    count = 0
    while count == 0:
        id_vk = input('Введите ID, либо username пользователя: ')
        vk_id = vk.VK(id_vk)
        if vk_id.user_get() == 1:
            count = 1

    count = 0
    while count == 0:
        id_yandex = input('Введите ID Yandex: ')
        ya_id = Yandex_api(id_yandex)
        my_answer = ya_id.upload_files_from_url()
        if my_answer == 201:
            count = 1
