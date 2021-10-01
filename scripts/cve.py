import json, requests, os
from dotenv import load_dotenv
from chrome_driver import driver
import models
from database import session, engine

load_dotenv()

models.Base.metadata.create_all(bind=engine)

cve_table = session.query(models.ScriptCve).all()

print("\nStarting script -> CVE" + "\n*******************\n")

for i in cve_table:
    cve_list = ""
    try:
        driver.implicitly_wait(3)
        driver.get(i.cve_url)
    except Exception as e:
        print(
            "\nApp Name: " + i.app_name.app_name,
            "\nURL: " + i.cve_url,
            "\n",
            e
        )
    index = [3,5,7,9]
    print("Getting the CVEs of " + i.app_name.app_name)
    for idx in index:
        try:
            cve_data = driver.find_element_by_xpath(i.cve_xpath % idx).text + "@@@" # add delimiter 
            cve_list += cve_data
        except Exception as e:
            print(
                "\nApp Name: " + i.app_name.app_name,
                "\nXPath: " + i.cve_xpath,
                "\n",
                e
            )

    # Send to API
    request_body = {
        "id_app": i.id_app,
        "cve": cve_list,
        "cve_link": i.cve_url
    }
    jsonData = json.dumps(request_body)
    headers = {
        'Content-Type': os.environ['HEADER'],
        'accept': os.environ['HEADER']
    }
    post_url = os.environ['CVE_POST_URL']
    sendData = requests.post(post_url, headers=headers, data=jsonData)

driver.quit()

print("\nOperation has finished" + "\n*******************")