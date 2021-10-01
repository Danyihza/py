from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import os
from dotenv import load_dotenv 

load_dotenv()

options = Options()
options.add_argument('--no-sandbox') # Bypass OS security model
options.add_argument('--disable-dev-shm-usage') # Overcome limited resource problem
options.add_argument('blink-settings=imagesEnabled=false') # Doesn't load images on browsing
options.add_argument('--headless') # Running in headless mode. Doesn't open chrome browser interactively

chromedriver_path = os.environ['CHROMEDRIVER_PATH']

DRIVER_PATH = chromedriver_path
driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)