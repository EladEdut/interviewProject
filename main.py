import json
import requests
from os import listdir, remove
from os.path import isfile, join, exists
from flask import Flask, request, jsonify
from bot import Bot
import pytest

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

path = r"C:\Users\Amir\PycharmProjects\interviewProject\bots"


def _get_bot_path(bot_name):
    return join(path, f"{bot_name}.json")


def _get_bot_list():
    bots_list = [f for f in listdir(path)]
    bots = []
    for bot in bots_list:
        with open(fr"{path}\{bot}") as con:
            content = json.load(con)
            bots.append(content)
    return bots


@app.route('/bots', methods=['POST'])
def create_bot():
    user_input = json.loads(request.json)
    new_bot = Bot(name=user_input["name"],
                  provider=user_input["provider"],
                  display_name=user_input["display_name"],
                  credentials=user_input["credentials"])
    with open(_get_bot_path(new_bot.get_name()), "w") as f:
        json.dump(new_bot.to_json(), f)
    return jsonify(new_bot.to_json()), 201


@app.route('/bots', methods=['GET'])
def get_bot_list():
    bots = _get_bot_list()
    return jsonify({"results": bots}), 200


@app.route('/bots/<bot_name>', methods=['GET'])
def get_bot(bot_name):
    bots = _get_bot_list()
    for bot in bots:
        if bot["name"] == bot_name:
            return jsonify({"result": bot}), 200
    return "Not Found", 404


@app.route('/bots/<bot_name>', methods=['DELETE'])
def delete_bot(bot_name):
    remove(_get_bot_path(bot_name))
    return "", 204


@app.route('/bots/<bot_name>', methods=['PUT'])
def change_bot(bot_name):
    user_input = request.json
    if 'provider' not in user_input or 'display_name' not in user_input or 'credentials' not in user_input:
        return "Must enter all fields for changing a bot", 400
    new_bot = Bot(name=user_input["name"],
                  provider=user_input["provider"],
                  display_name=user_input["display_name"],
                  credentials=user_input["credentials"])
    with open(_get_bot_path(bot_name), "w") as f:
        json.dump(new_bot.to_json(), f)
    print(f"{bot_name} was updated")
    return "", 204


@app.route('/bots/<bot_name>', methods=['PATCH'])
def update_bot(bot_name):
    user_input = request.json
    with open(_get_bot_path(bot_name), "r") as f:
        bot = json.load(f)
    for key, value in user_input.items():
        if value == "":
            pass
        else:
            bot[key] = value
    with open(fr"{path}\{bot_name}.json", "w") as f:
        json.dump(bot, f)
    return "", 204


if __name__ == '__main__':
    app.run(debug=True, port=8000)
