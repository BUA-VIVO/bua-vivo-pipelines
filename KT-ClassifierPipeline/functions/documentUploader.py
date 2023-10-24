# -*- coding: utf-8 -*-
from datetime import datetime
import time
from dotenv import load_dotenv
import os
import requests


def load_envs():
    load_dotenv()



def upload_document(project_id, file_path, arguments, user, password, index):

    if not wait_for_job():

        endpoint = os.getenv("HOST_URL")+"/"+os.getenv("IMPORT_PATH")+os.getenv("URI_VARS")
        print("CONTACTING ENDPOINT: " + endpoint)
        post_response = requests.post(
            url=endpoint,
            files={'file': (index + "_Classified_" + str(datetime.today().strftime('%Y-%m-%d')) + "_documents.json"
                            , open(file_path, 'rb'))},
            auth=(user, password))

        if post_response.status_code == 200:
            print("Imported " + str(file_path))
        else:
            print(post_response.status_code + " : There was a problem")


def wait_for_job():
    print("hosturl")
    print("WAITING")
    print(os.getenv("HOST_URL"))
    waitfor=True
    while waitfor:
        get_response = requests.get(
            url=os.getenv("HOST_URL")+"/"+os.getenv("JOB_PATH"),
            auth=(os.getenv("ADMIN_USER"), os.getenv("ADMIN_PASS")))

        if get_response.status_code == 200:
            if get_response.text == "[ ]":
                waitfor=False
                break
            else:
                time.sleep(int(os.getenv("SLEEP_TIME")))

    return waitfor






