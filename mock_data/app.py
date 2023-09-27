# app.py
# эмулирует работу трассира
import os

from flask import Flask, jsonify, request, send_file
import random
import cv2

guids = [
    [{'Окно 1': 'AIhKLrez'}, {'Окно 2': 'Aqi3PH68'}, {'Окно 3': 'Axqo72v1'}],
    [{'Окно 1': 'CcSdeDso'}, {'Окно 2': 'CfRMLrYx'}, {'Окно 3': 'DZfSh12w'}]
]
password = "masha"



app = Flask(__name__)


@app.route('/objects/', methods=['GET'])
# http://localhost:5000/objects/?password=123
def get_objects():

    if request.args.get('password') == password:
        return jsonify(guids[random.randint(0, 0)])

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
# Пример использования функции

def extract_random_frame(video_path = "video1.avi"):
    # Открываем видеофайл

    cap = cv2.VideoCapture(video_path)

    # Получаем общее количество кадров в видео
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Генерируем случайный номер кадра
    random_frame_number = random.randint(0, frame_count - 1)

    # Устанавливаем текущий кадр на случайный кадр
    cap.set(cv2.CAP_PROP_POS_FRAMES, random_frame_number)

    # Считываем случайный кадр
    ret, frame = cap.read()
    # cv2.imshow("output_path", frame)
    # Если кадр считан успешно, сохраняем его как изображение
    if ret:
        return frame
    else:
        print("no ret")
        return None

@app.route('/screenshot/<guid>', methods=['GET'])
# http://localhost:5000/screenshot/AIhKLrez?password=123
def get_screenshot(guid):

    if request.args.get('password') == password:

        data = list(map(lambda d: list(d.values())[0], guids[random.randint(0, 0)]))
        if guid in data:
            cv2.imwrite('temporary_frame.jpg', extract_random_frame())

            # Отправляем временное изображение с помощью Flask
            return send_file('temporary_frame.jpg', mimetype='image/jpeg')
            # return send_file(extract_random_frame(), mimetype='image/jpg')

        return jsonify({"error": "need to finish it!"}), 403

    # Если GUID или пароль неправильные, возвращаем ошибку
    return jsonify({"error": "Invalid GUID or password"}), 401

if __name__ == '__main__':
    app.run(debug=True)
