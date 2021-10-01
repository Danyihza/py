import json, requests, os
from dotenv import load_dotenv
from chrome_driver import driver
import models
from database import session, engine

load_dotenv()

models.Base.metadata.create_all(bind=engine)

latest_ver_table = session.query(models.ScriptLatest).all()

print("\nStarting script -> LATEST_VERSION" + "\n*******************\n")

for i in latest_ver_table:
    latest_ver_data = ""
    release_notes_data = i.release_notes_url

    print("Getting the Latest Version and Release Notes of " + i.app_name.app_name)
    try:
        driver.implicitly_wait(3)
        driver.get(i.latest_url)
    except Exception as e:
        print(
            "\nApp Name: " + i.app_name.app_name,
            "\nURL: " + i.latest_url,
            "\n",
            e
        )
    if i.type == "element":
        try:
            latest_ver_data = driver.find_element_by_xpath(i.latest_xpath).text
        except Exception as e:
            print(
                "\nApp Name: " + i.app_name.app_name,
                "\nXPath: " + i.latest_xpath,
                "\n",
                e,
            )

    # Send to API
    request_body = {
        "id_app": i.id_app,
        "latest_version": latest_ver_data,
        "release_notes": release_notes_data
    }
    json_data = json.dumps(request_body)
    headers = {
        'Content-Type': os.environ['HEADER'],
        'accept': os.environ['HEADER']
    }
    post_url = os.environ['LATEST_POST_URL']
    sendData = requests.post(post_url, headers=headers, data=json_data)

driver.quit()

print("\nOperation has finished" + "\n*******************")