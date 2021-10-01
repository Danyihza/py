import json, requests, os
from dotenv import load_dotenv
import models
from database import session, engine

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app_name_table = session.query(models.AppName).all()

print("\nStarting script -> APP_NAMES" + "\n*******************\n")

for i in app_name_table:
    # Send to API
    request_body = {
        "app_name": i.app_name
    }
    jsonData = json.dumps(request_body)
    headers = {
        'Content-Type': os.environ['HEADER'],
        'accept': os.environ['HEADER']
    }
    post_url = os.environ['APP_POST_URL']
    sendData = requests.post(post_url, headers=headers, data=jsonData)

print("\nOperation has finished" + "\n*******************")