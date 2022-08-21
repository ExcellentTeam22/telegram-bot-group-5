import io

from flask import Flask, Response, request
import face_recognition
import requests
import numpy as np
from PIL import Image

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

ACCEPT_MESSAGE = "אני 052-538-164-8"
DECLINE_MESSAGE = "!מי זאת"

app = Flask(__name__)
TOKEN = '5696168580:AAHuXW8Jd0lZjYROK4cgpPEfEsOXhOxbEOE'
NGROK = 'https://c0a8-82-80-173-170.eu.ngrok.io'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url={}/message'.format(TOKEN, NGROK)
requests.get(TELEGRAM_INIT_WEBHOOK_URL)


@app.route('/sanity')
def sanity(): return "Server is running"


@app.route('/message', methods=["POST"])
def handle_message():
    print("got message")
    json = request.get_json()
    print(json)
    chat_id = json['message']['chat']['id']
    if 'photo' not in json['message']:
        res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'".format(TOKEN, chat_id,
                                                                                                   DECLINE_MESSAGE))
        return Response("failure")
    message = json['message']['photo']
    pic_file_path = requests.get('https://api.telegram.org/bot{}/getfile?file_id={}'.format(TOKEN, message[0]['file_id'])).json()['result']['file_path']
    downloaded_pic = requests.get('https://api.telegram.org/file/bot{}/{}'.format(TOKEN, pic_file_path)).content
    known_face = face_recognition.face_encodings(face_recognition.load_image_file("resources/4.jpg"))[0]
    image = Image.open(io.BytesIO(downloaded_pic))
    pic = np.array(image)
    unknown_faces = face_recognition.face_encodings(pic)
    match_results = [unknown_face for unknown_face in unknown_faces
                        if face_recognition.compare_faces([known_face], unknown_face)]
    res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'".format(TOKEN, chat_id,
                                                                                               ACCEPT_MESSAGE
                                                                                               if len(match_results) >= 1 else DECLINE_MESSAGE))
    return Response("success")


if __name__ == '__main__':
    app.run(port=5002)
