# Python program to read
# json file

import json
import requests
import os
from pymongo import MongoClient
import urllib.parse
import argparse
import comtypes.client as cc
import comtypes
import io

collection = "event_video-2022-04"

####################################################__FUNCTION__######################################################


def get_database():

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['admin']


def send_link_to_idm(link, file_name=None):
    bstrUrl = link
    bstrReferer = ""
    bstrCookies = ""
    bstrData = ""
    bstrUser = ""
    bstrPassword = ""
    bstrLocalPath = ""
    bstrLocalFileName = "" if file_name is None else file_name
    lFlags = 3
    reserved1 = comtypes.automation.VARIANT(0)
    reserved2 = comtypes.automation.VARIANT(0)

    idm_tlb_path = "C:\\Program Files (x86)\\Internet Download Manager\\idmantypeinfo.tlb"
    if not os.path.exists(idm_tlb_path):
        idm_tlb_path = "C:\\Program Files\\Internet Download Manager\\idmantypeinfo.tlb"
    # cc.GetModule("C:\\Program Files (x86)\\Internet Download Manager\\idmantypeinfo.tlb")
    cc.GetModule(idm_tlb_path)
    # not sure about the syntax here, but cc.GetModule will tell you the name of the wrapper it generated
    import comtypes.gen.IDManLib as IDMan
    idm1 = cc.CreateObject("IDMan.CIDMLinkTransmitter",
                           None, None, IDMan.ICIDMLinkTransmitter2)

    idm1.SendLinkToIDM2(bstrUrl, bstrReferer, bstrCookies, bstrData, bstrUser,
                        bstrPassword, bstrLocalPath, bstrLocalFileName, lFlags,
                        reserved1, reserved2)


def get_video(file_name):
    print("Get video to download")
    if not os.path.exists("video/video_to_download.txt"):
        count = 1
        arr = []

        f = open(file_name, encoding='utf-8')

        data = json.load(f)
        size = len(data)

        dbname = get_database()
        collection_name = dbname[collection]

        for i in data:
            item_details = collection_name.find(
                {"timestamp": {"$lte": i["timestamp"]}}).sort("timestamp", -1)
            arr.append(item_details[0]["file"])

            print(str(count) + "/" + str(size) +
                  ": " + item_details[0]["file"])
            count += 1

        if not os.path.exists("video/"):
            os.makedirs("video/")

        arr = list(dict.fromkeys(arr))

        t = open("video/video_to_download.txt", "w")

        for i in arr:
            t.write(i)
            t.write("\n")

        t.close()

        f.close()


def get_link():
    print("Get link of video")
    arr = []
    count = 1

    url = "https://api-camera.hanet.ai/v3/video/getVideoLinkByFile"

    f = open('video/video_to_download.txt', encoding='utf-8')

    lines = f.readlines()
    size = len(lines)

    for i in lines:
        payload = 'userID=1495348707219832832&session=6dbfb0f0-32ac-4094-9d7b-42baf8fbfb52&date=2022-03-15&deviceID={}&file={}&type=s3'.format(
            i[1:11], urllib.parse.quote(i[:46], safe=""))
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        arr.append(response.json()['data']['link'])
        print(str(count) + "/" + str(size) + " item added")
        count += 1

    arr = list(dict.fromkeys(arr))

    count = 1

    if not os.path.exists("video/"):
        os.makedirs("video/")

    t = open("video/video_link.txt", "w")
    skip = 1
    for i in arr:
        if skip == 10:
            t.write(i)
            t.write("\n")
            print(str(count) + "/" + str(size) + " item writed")
            count += 1
            skip += 1
            if count == 41:
                break
        elif skip < 10:
            skip += 1
            continue
        else:
            skip = 1
            continue

    t.close()

    print("complete")


def send_link():
    print("Send link of video to IDM")
    count = 1

    f = open('video/video_link.txt', encoding='utf-8')

    lines = f.readlines()
    size = len(lines)

    for i in lines:

        send_link_to_idm(i, i[89:112])

        print(str(count) + "/" + str(size) + " video downloaded")
        count += 1

    print("Downloaded all video")


#####################################################__MAIN__#############################################################


def main():

    get_video("json/tracking-2022-04.json")
    get_link()
    send_link()


if __name__ == "__main__":
    main()
