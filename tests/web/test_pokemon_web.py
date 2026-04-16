"""
Smoke tests for pokemons
"""

import pytest
import requests

from loguru import logger

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common.conf import Cfg

class Locators:

    EMAIL = '[class*="k_form_f_email"][id="k_email"]'
    PASSWORD = '[class*="k_form_f_pass"][id="k_password"]'
    LOGIN = '[class*="k_form_send_auth"]'
    TRAINER_ID = '[class*="header_card_trainer_id_num"]'
    ALERT = '[class*="auth__error"]'
    POK_COUNT = '[class*="total-count history-info_count"]'


def test_positive_login(browser):
    """
    POC-1. Positive case
    """

    browser.get(url=f'{Cfg.URL}/login')

    logger.info('Step 1. Wait for clickable email input, type email and password')
    email = WebDriverWait(browser, timeout=10, poll_frequency=2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, Locators.EMAIL)))
    email.click()
    email.send_keys(Cfg.VALID['email'])

    password = browser.find_element(by=By.CSS_SELECTOR, value=Locators.PASSWORD)
    password.click()
    password.send_keys(Cfg.VALID['password'])

    logger.info('Step 2. Press Enter to login')
    enter = browser.find_element(by=By.CSS_SELECTOR, value=Locators.LOGIN)
    enter.click()

    WebDriverWait(browser, timeout=10, poll_frequency=2).until(EC.url_to_be(f'{Cfg.URL}/'))

    logger.info('Step 3. Find trainer ID')
    trainer_id = browser.find_element(by=By.CSS_SELECTOR, value=Locators.TRAINER_ID)
    assert trainer_id.text == Cfg.TRAINER_ID, 'Unexpected ID trainer'

CASES = [
    ('1', Cfg.INVALID['email'], Cfg.VALID['password'], 'Введите корректную почту'),
    ('2', Cfg.VALID['email'], Cfg.INVALID['password'], 'Неверные логин или пароль'),
    ('3', '', Cfg.VALID['password'], 'Введите почту'),
    ('4', Cfg.VALID['email'], '', 'Введите пароль')
]

@pytest.mark.parametrize('case_number, email, password, alerts', CASES)
def test_negative_login(case_number, email, password, alerts, browser):
    """
    POC-2. Negative cases
    """
    logger.info(f'Negative case № {case_number}')
    browser.get(url=Cfg.URL)
   
    WebDriverWait(browser, timeout=10, poll_frequency=2).until(EC.url_to_be(f'{Cfg.URL}/login'))

    email_input = browser.find_element(by=By.CSS_SELECTOR, value = Locators.EMAIL)
    email_input.click()
    email_input.send_keys(email)

    password_input = browser.find_element(by=By.CSS_SELECTOR, value = Locators.PASSWORD)
    password_input.click()
    password_input.send_keys(password)

    enter_button = browser.find_element(by=By.CSS_SELECTOR, value = Locators.LOGIN)
    enter_button.click()

    alert = WebDriverWait(browser, timeout=10, poll_frequency=2).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, Locators.ALERT)))

    assert alert.text == alerts, 'Unexpected alerts in authentication form'

# @pytest.mark.xfail(reason="Wait for fix bug #12345")
def test_check_api(browser, knockout):
    """
    POC-3. Check API
    """
    
    browser.get(url=Cfg.URL)
    WebDriverWait(browser, timeout=10, poll_frequency=2).until(EC.url_to_be(f'{Cfg.URL}/login'))

    email_input = browser.find_element(by=By.CSS_SELECTOR, value = Locators.EMAIL)
    email_input.click()
    email_input.send_keys(Cfg.VALID['email'])

    password_input = browser.find_element(by=By.CSS_SELECTOR, value = Locators.PASSWORD)
    password_input.click()
    password_input.send_keys(Cfg.VALID['password'])

    browser.find_element(by=By.CSS_SELECTOR, value= Locators.LOGIN).click()

    WebDriverWait(browser, timeout=10, poll_frequency=2).until(EC.url_to_be(f'{Cfg.URL}/'))
    browser.find_element(by=By.CSS_SELECTOR, value = '[class*="header_card_trainer_id_num"]').click()
    WebDriverWait(browser, timeout=10, poll_frequency=2).until(EC.url_to_be(f'{Cfg.URL}/trainer/{Cfg.TRAINER_ID}'))

    pok = WebDriverWait(browser, timeout=10, poll_frequency=2).until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, '[class*="pokemon_one_body_content_inner_pokemons"]')))
    WebDriverWait(browser, timeout=10, poll_frequency=2).until(
        lambda x: 'feature-empty' not in pok.get_attribute('class'))

    pokemon_count_before = browser.find_element(by=By.CSS_SELECTOR, value = Locators.POK_COUNT)
    count_before = int(pokemon_count_before.text)
    
    body_create = {
        "name": "generate",
        "photo_id": -1
    }
    header = {'Content-Type':'application/json','trainer_token': Cfg.TRAINER_TOKEN}
    responce_create = requests.post(url=f'{Cfg.API_URL}/pokemons', headers = header, params = Cfg.TRAINER_ID, json= body_create, timeout=3)

    assert responce_create.status_code == 201, 'Unexpected status code'

    browser.refresh()
    assert WebDriverWait(browser, timeout=5, poll_frequency=1).until(EC.text_to_be_present_in_element(
        (By.CSS_SELECTOR, Locators.POK_COUNT), f'{count_before+1}')), 'Unexpected pokemons count'
