from pyvirtualdisplay import Display
from selenium import webdriver
import os


def init_driver() -> webdriver:
    if 'MAC' not in os.environ:
        print("Initializing display")
        display = Display(visible=False, size=(1200, 1200))
        display.start()
        print("Display initialized")

    # Create a new Chrome session
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    print("Initializing Chromedriver")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(30)
    driver.maximize_window()
    print("Chromedriver initialized")

    return driver
