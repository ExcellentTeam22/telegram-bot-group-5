import io

import waitress

import config
from flask import Flask, Response, request
import face_recognition
import requests
import numpy as np
from PIL import Image

ACCEPT_MESSAGE = "אני 052-538-164-8"
DECLINE_MESSAGE = "!מי זאת"

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
TOKEN = 'TELEGRAM BOT TOKEN'
NGROK = 'NGROK ADDRESS'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url={}/message'.format(TOKEN, NGROK)
requests.get(TELEGRAM_INIT_WEBHOOK_URL)

@app.route('/message', methods=["POST"])
def handle_message():
    json = request.get_json()
    if 'message' not in json:
        return Response("failure")
    chat_id = json['message']['chat']['id']
    if 'photo' not in json['message']:
        res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(TOKEN, chat_id,                                                                                                   DECLINE_MESSAGE))
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
    res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(TOKEN, chat_id,
                                                                                               ACCEPT_MESSAGE
                                                                                               if match_results else DECLINE_MESSAGE))
    return Response("success")


if __name__ == '__main__':
    waitress.serve(app, port="5002")
