import requests
import pytest

from common.conf import Cfg


HEADER = {"Content-Type": "application/json", "trainer_token": Cfg.TRAINER_TOKEN}

def test_trainers_status_code():
    responce = requests.get(url = f'{Cfg.API_URL}/trainers', headers= HEADER)
    assert responce.status_code == 200

def test_query_trainer():
    responce_query_check = requests.get(url = f'{Cfg.API_URL}/trainers', headers= HEADER, params = {"trainer_id": Cfg.TRAINER_ID})
    assert responce_query_check.json()["data"][0]["id"] == Cfg.TRAINER_ID