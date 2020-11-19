import pytest
import requests
from bot import Bot

class Test:

    def test_post(self):
        bot_post = Bot("a", "b", "c", "d")
        assert requests.post(fr"C:\Users\Amir\PycharmProjects\interview_project\bots\{bot_post.get_name()}.json", json=bot_post.to_json() )