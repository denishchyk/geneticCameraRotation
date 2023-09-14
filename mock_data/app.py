# app.py
# эмулирует работу трассира
import os

from flask import Flask, jsonify, request, send_file
import random

guids = [
    [{'Окно 1': 'AIhKLrez'}, {'Окно 2': 'Aqi3PH68'}, {'Окно 3': 'Axqo72v1'}],
    [{'Окно 1': 'CcSdeDso'}, {'Окно 2': 'CfRMLrYx'}, {'Окно 3': 'DZfSh12w'}]
]
password = "123"



app = Flask(__name__)


@app.route('/objects/', methods=['GET'])
# http://localhost:5000/objects/?password=123
def get_objects():

    if request.args.get('password') == password:
        return jsonify(guids[random.randint(0, 1)])

    # Если GUID или пароль неправильные, возвращаем ошибку
    return jsonify({"error": "Invalid GUID or password"}), 401

def send_photo():

    image_directory = 'out'
    # return send_file('abc.png', mimetype='image/png')
    image_files = [f for f in os.listdir(image_directory)]
    # Select a random image file
    random_image_file = random.choice(image_files)

    # Define the full path to the selected image
    image_path = os.path.join(image_directory, random_image_file)
    return image_path

@app.route('/screenshot/<guid>', methods=['GET'])
# http://localhost:5000/screenshot/AIhKLrez?password=123
def get_screenshot(guid):

    if request.args.get('password') == password:

        data = list(map(lambda d: list(d.values())[0], guids[random.randint(0, 1)]))
        if guid in data:
            return send_file(send_photo(), mimetype='image/png')

        return jsonify({"error": "need to finish it!"}), 403

    # Если GUID или пароль неправильные, возвращаем ошибку
    return jsonify({"error": "Invalid GUID or password"}), 401

if __name__ == '__main__':
    app.run(debug=True)
