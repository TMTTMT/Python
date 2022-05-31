
import json
from multiprocessing import Process
import requests
import os
from pymongo import MongoClient

# Constant

url_tracking = "https://s3.ap-northeast-1.wasabisys.com/camera.vn.hcm/license/upload"
url_person = "https://static.hanet.ai/face/employee"
url_plate = "https://s3.ap-northeast-1.wasabisys.com/camera.vn.hcm/license/upload"


####################################################__FUNCTION__######################################################


def download_plate(file_name):
    count = 1

    f = open(file_name, encoding='utf-8')

    data = json.load(f)
    size = len(data)

    for i in data:

        try:
            if os.path.exists("image/plate/" + i["data"]["code_result"] + ".jpg"):
                continue

            if not os.path.exists("image/plate/"):
                os.makedirs("image/plate/")

            downloadLink = url_plate + i["url"]

            response = requests.get(downloadLink)

            file = open("image/plate/" + i["data"]
                        ["code_result"] + ".jpg", "wb")
            file.write(response.content)
            file.close()

            print(str(count) + "/" + str(size) + ": image/plate/" +
                  i["data"]["code_result"] + ".jpg")
            count += 1

        except:
            print(i)

    print("\nDone download image\n")

    f.close()


def download_car(file_name):
    count = 1

    f = open(file_name, encoding='utf-8')

    data = json.load(f)
    size = len(data)

    for i in data:

        try:
            if os.path.exists("image/car/" + i["fileName"]):
                continue

            if not os.path.exists("image/car/"):
                os.makedirs("image/car/")

            downloadLink = url_plate + i["url"]

            response = requests.get(downloadLink)

            file = open("image/car/" + i["fileName"], "wb")
            file.write(response.content)
            file.close()

            print(str(count) + "/" + str(size) +
                  ": image/car/" + i["fileName"])
            count += 1

        except:
            print(i)

    print("\nDone download image\n")

    f.close()


#####################################################__MAIN__#############################################################


def main():
    plate = "json/tracking-2022-05-13-005.json"
    # car = "vehicle.json"

    p1 = Process(target=download_plate, args=(plate,)).start()
    # p2 = Process(target=download_car, args=(car,)).start()

    print("Program complete")


if __name__ == "__main__":
    main()
