import requests
import datetime
import json
from tqdm import tqdm
TOKEN = ""
user_id = input()
API_BASE_URL = "https://api.vk.com/method/photos.get"
token = input()


def get_common_params():
    return {
        "access_token": TOKEN,
        "v": "5.131"
    }


def max_size_photo():
    params = get_common_params()
    params.update({"owner_id": user_id,
                   "album_id": "profile",
                   'photo_sizes': 1,
                   'extended': 1
                   })
    response = requests.get(API_BASE_URL, params=params)
    photos = response.json()["response"]["items"]
    max_size_photos = {}
    for photo in photos:
        max_size = sorted(photo['sizes'], key=lambda x: x['width'] * x['height'])[-1]
        file_name = str(photo["likes"]["count"])
        upload_date = datetime.datetime.fromtimestamp(photo["date"]).strftime("%Y.%m.%d")
        if file_name in max_size_photos:
            file_name += "_" + upload_date
        max_size_photos[file_name] = {
            "url": max_size["url"],
            "size": max_size['type']
        }

    return max_size_photos


def save_photo():
    url = "https://cloud-api.yandex.net/v1/disk/resources"
    headers = {"Authorization": "OAuth {}".format(token)}
    path = "Photo_vk/"
    params = {"path": path}
    response = requests.put(url, headers=headers, params=params)
    photos = max_size_photo()
    info_photo = []
    progress_bar = tqdm(total=len(photos))
    for photo, photo_url in photos.items():
        url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        url_photo = photo_url['url']
        size = photo_url['size']
        params = {"url": url_photo, "path": path + photo}
        response = requests.post(url, headers=headers, params=params)
        info_photo.append({
            "file_name": photo,
            'size': size})
        file_ = info_photo
        with open("file_.json", "w") as file:
            json.dump(file_, file)
        progress_bar.update(1)
    progress_bar.close()


save_photo()