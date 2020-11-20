import pytest
import requests
import json
from os.path import isfile, join, exists
from bot import Bot

from tests.utils import hash_collection, hash_dict, get_random_name

path = r"C:\Users\Amir\PycharmProjects\interviewProject\bots"
URL = "http://localhost:8000/bots"


def _get_random_bot_name():
    return get_random_name("bot")


def _get_bot_url(bot_name):
    return f"{URL}/{bot_name}"


def _create_bot(new_bot):
    bot_json = json.dumps(new_bot)
    creation_response = requests.post(URL, json=bot_json)
    status = creation_response.status_code
    assert status == 201
    return creation_response.json()


def _check_existence(bot):
    new_item_hash = hash_dict(bot)
    all_bots = requests.get(URL).json()
    all_bots_list = all_bots["results"]
    all_bot_hashes = [hash_dict(i) for i in all_bots_list]
    return new_item_hash in all_bot_hashes


def test_creation_and_listing():
    new_bot_data = {"credentials": "C",
                    "display_name": "Bot_3",
                    "name": _get_random_bot_name(),
                    "provider": "a"}
    new_bot = _create_bot(new_bot_data)
    assert _check_existence(new_bot)


def test_delete():
    bot_name = _get_random_bot_name()
    new_bot = {"credentials": "D",
               "display_name": "Bot_Z",
               "name": bot_name,
               "provider": "c"}
    new_bot_item = _create_bot(new_bot)
    assert _check_existence(new_bot_item)
    requests.delete(_get_bot_url(bot_name))
    assert not _check_existence(new_bot_item)


def test_put():
    bot_name = _get_random_bot_name()
    bot_data = {
        "credentials": "U",
        "display_name": "Bot_P",
        "name": bot_name,
        "provider": "p"
    }
    creation_result = _create_bot(bot_data)
    bot_data["display_name"] = "Bot_C"
    requests.put(_get_bot_url(bot_name), json=bot_data)
    updated_bot = requests.get(_get_bot_url(bot_name)).json()
    assert hash_dict(updated_bot["result"]) == hash_dict(bot_data)
    assert hash_dict(updated_bot["result"]) != hash_dict(creation_result)


def test_put_partial():
    # testing partial input when changing the whole bot
    bot_name = _get_random_bot_name()
    bot_data = {
        "credentials": "U",
        "display_name": "Bot_P",
        "name": bot_name,
        "provider": "p"
    }
    creation_result = _create_bot(bot_data)
    bot_data = {
        "credentials": "",
        "display_name": "Bot_E",
        "name": bot_name,
        "provider": ""
    }
    put_response = requests.put(_get_bot_url(bot_name), json={
        "display_name": bot_data["display_name"],
        "name": bot_name
    })
    updated_bot = requests.get(_get_bot_url(bot_name)).json()
    assert put_response.status_code == 400
    assert hash_dict(updated_bot["result"]) == hash_dict(creation_result)


def test_patch():
    bot_name = _get_random_bot_name()
    bot_data = {
        "credentials": "I",
        "display_name": "Bot_V",
        "name": bot_name,
        "provider": "k"
    }
    creation_result = _create_bot(bot_data)
    bot_data = {
        "credentials": "",
        "display_name": "Bot_Q",
        "name": bot_name,
        "provider": ""
    }
    requests.patch(_get_bot_url(bot_name), json={
        "display_name": bot_data["display_name"],
        "name": bot_name
    })
    updated_bot = requests.get(_get_bot_url(bot_name)).json()
    assert hash_dict(updated_bot["result"]) != hash_dict(bot_data)
    assert hash_dict(updated_bot["result"]) != hash_dict(creation_result)
