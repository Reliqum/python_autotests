"""
Configuration test
"""

import pytest
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from common.conf import Cfg

@pytest.fixture(scope="function")
def browser():
    """
    Main fixture
    """
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("start-maximized") # Open browser in maximized mode
    chrome_options.add_argument("--disable-infobars") # Disabling infobars
    chrome_options.add_argument("--disable-extensions") # Disabling extensions
    chrome_options.add_argument("--disable-gpu") # Applicable only to Windows OS
    chrome_options.add_argument("--disable-dev-shm-usage") # Overcome limited resource problem
    # chrome_options.add_argument("--headless") # Browser control using API

    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def knockout():
    """
    Knockout all pokemons
    """
    header = {'Content-Type':'application/json','trainer_token': Cfg.TRAINER_TOKEN}
    pokemons = requests.get(url=f'{Cfg.API_URL}/pokemons', params={"trainer_id": Cfg.TRAINER_ID},
                            headers=header, timeout=3)
    if 'data' in pokemons.json():
        for pokemon in pokemons.json()['data']:
            if pokemon['status'] != 0:
                requests.post(url=f'{Cfg.API_URL}/pokemons/knockout', headers=header,
                              json={"pokemon_id": pokemon['id']}, timeout=3)