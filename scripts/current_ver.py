import json, requests, os
from dotenv import load_dotenv
from chrome_driver import driver
import models
from database import session, engine

load_dotenv()

models.Base.metadata.create_all(bind=engine)

current_table_all = session.query(models.ScriptCurrent).all()
current_id_app = []

for i in current_table_all:
    current_id_app.append(i.id_app)

unique_id_app = list(set(current_id_app))

print("\nStarting script -> CURRENT_VERSION" + "\n*******************\n")

for i in unique_id_app:
    current_list = ""
    keterangan_list = ""
    current_table = session.query(models.ScriptCurrent).filter(
        models.ScriptCurrent.id_app == i
    ).all()

    for j in current_table:
        if j.type == "element":
            keterangan_list += j.current_url + "@@@"  # add delimiter
            try:
                driver.implicitly_wait(3)
                driver.get(j.current_url)
            except Exception as e:
                print(
                    "\nApp Name: " + j.app_name.app_name,
                    "\nURL: " + j.current_url,
                    "\n",
                    e
                )
            print("Getting the Current Versions of " + j.app_name.app_name)

            try:
                current_data = driver.find_element_by_xpath(j.current_selector).text + "@@@"
                current_list += current_data
            except Exception as e:
                print(
                    "\nApp Name: " + j.app_name.app_name,
                    "\nXPath: " + j.current_selector,
                    "\n",
                    e
                )

        elif j.type == "x-jenkins":
            keterangan_list += j.current_url + "@@@"
            print("Getting the Current Versions of " + j.app_name.app_name)
            response = requests.head(j.current_url)

            response_dict = {
                'http_status_code': response.status_code,
                'headers': {k.lower(): v for (k,v) in response.headers.items()} 
            }

            jenkins_version = response_dict['headers']['x-jenkins'] + "@@@"
            current_list += jenkins_version

        elif j.type == "api-prometheus":
            print("Getting the Current Versions of " + j.app_name.app_name)
            response = requests.get(j.current_url + j.current_selector).text
            result = json.loads(response)
            result_list = result['data']['result']

            for idx in result_list:
                # Get Current Version
                tmp = idx['metric']
                if 'short_version' not in tmp:
                    current_list += tmp['version'] + "@@@"
                elif 'short_version' in tmp:
                    current_list += tmp['short_version'] + "@@@"
                else: 
                    print("No version found")

                # Get Keterangan data
                if tmp['__name__'] == "prometheus_build_info":
                    keterangan_list += j.current_url + "@@@"
                elif 'kubernetes_pod_name' in tmp:
                    keterangan_list += tmp['kubernetes_pod_name'] + "@@@"
                elif 'instance_name' in tmp:
                    keterangan_list += tmp['instance_name'] + "@@@"
                else:
                    print("No application name found")

        elif j.type == "api-simple":
            print("Getting the Current Versions of " + j.app_name.app_name)
            response = requests.get(j.current_url + j.current_selector).text
            current_list += response + "@@@"
            keterangan_list += j.current_url

    # Send to API
    request_body = {
        "id_app": i,
        "current_version": current_list,
        "keterangan": keterangan_list
    }
    jsonData = json.dumps(request_body)
    headers = {
        'Content-Type': os.environ['HEADER'],
        'accept': os.environ['HEADER']
    }
    post_url = os.environ['CURRENT_POST_URL']
    sendData = requests.post(post_url, headers=headers, data=jsonData)

driver.quit()

print("\nOperation has finished" + "\n*******************")