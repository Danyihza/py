## File Structure
```
├── .env  
├── main.py  
├── nginx-unit  
│   └── config.json  
├── requirements.txt  
├── scripts  
│   ├── app_name.py  
│   ├── chrome_driver.py  
│   ├── current_ver.py  
│   ├── cve.py  
│   ├── database.py  
│   ├── .env  
│   ├── latest_ver.py  
│   └── models.py  
└── sql_app  
    ├── crud.py  
    ├── database.py  
    ├── __init__.py  
    ├── models.py  
    └── schemas.py  
```
## scripts folder  
Where the scripts to get the necessary data (Current Version, Latest Version, etc) lies.  
It uses variables inside the PostgreSQL database  
  
The scripts works independently and has no relation to the main FastAPI App.

## sql_app folder
The main backbone of the FastAPI app. Using PostgreSQL to store data.  
All of the process inside this will be used by the main.py file.  