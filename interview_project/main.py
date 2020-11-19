import json
from os import listdir, remove
from os.path import isfile, join, exists
from flask import Flask, request, jsonify
from bot import Bot

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


@app.route('/bot/create', methods=['POST'])
def create_bot():
    user_input = request.json
    new_bot = Bot(user_input["provider"], user_input["name"], user_input["display_name"], user_input["credentials"])
    with open(fr"C:\Users\Amir\PycharmProjects\interview_project\bots\{new_bot.get_name()}.json", "w") as f:
        json.dump(new_bot.to_json(), f)
    return jsonify(new_bot.to_json()), 201


@app.route('/bot/all_bots', methods=['GET'])
def get_bot_list():
    path = r"C:\Users\Amir\PycharmProjects\interview_project\bots"
    bots_list = [f for f in listdir(path)]
    output = []
    for bot in bots_list:
        with open(fr"{path}\{bot}") as con:
            content = json.load(con)
            output.append(content)
    return output, 201


@app.route('/bot/<bot_name>/delete', methods=['DELETE'])
def delete_bot(bot_name):
    remove(f"{bot_name}.json")
    return jsonify({"done": f"{bot_name} was deleted"}), 204


@app.route('/bot/<bot_name>/put', methods=['PUT'])
def change_bot(bot_name):
    user_input = request.json
    new_bot = Bot(user_input["provider"], bot_name, user_input["display_name"], user_input["credentials"])
    with open(fr"C:\Users\Amir\PycharmProjects\interview_project\bots\{bot_name}.json", "w") as f:
        json.dump(new_bot.to_json(), f)
    print(f"{bot_name} was updated")
    return jsonify({"done": f"{bot_name} was updated"}), 204


@app.route('/bot/<bot_name>/patch', methods=['PATCH'])
def update_bot(bot_name):
    user_input = request.json
    with open(fr"C:\Users\Amir\PycharmProjects\interview_project\bots\{bot_name}.json", "r") as f:
        bot = json.loads(f)
    for key, value in user_input.items():
        bot[key] = value
    with open(fr"C:\Users\Amir\PycharmProjects\interview_project\bots\{bot_name}.json", "w") as f:
        json.dump(bot, f)
    return jsonify({"done": f"{bot_name} was updated"}), 204


if __name__ == '__main__':
    app.run(debug=True, port=8000)
