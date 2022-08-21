import io

from flask import Flask, Response, request
import face_recognition
import requests
import numpy as np
from PIL import Image

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
TOKEN = '5696168580:AAHuXW8Jd0lZjYROK4cgpPEfEsOXhOxbEOE'
NGROK = 'https://ea35-82-80-173-170.eu.ngrok.io'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url={}/message'.format(TOKEN, NGROK)
requests.get(TELEGRAM_INIT_WEBHOOK_URL)


@app.route('/sanity')
def sanity(): return "Server is running"


@app.route('/message', methods=["POST"])
def handle_message():
    print("got message")
    json = request.get_json()
    chat_id = json['message']['chat']['id']
    message = json['message']['photo']
    print(json)
    print('https://api.telegram.org/bot{}/getfile?file_id={}'.format(TOKEN, message[0]['file_id']))
    pic = requests.get('https://api.telegram.org/bot{}/getfile?file_id={}'.format(TOKEN, message[0]['file_id']))
    pic_file_path = pic.json()['result']['file_path']
    downloaded_pic = requests.get('https://api.telegram.org/file/bot{}/{}'.format(TOKEN, pic_file_path)).content
    known_face = face_recognition.face_encodings(face_recognition.load_image_file("resources/4.jpg"))[0]
    image = Image.open(io.BytesIO(downloaded_pic))
    pic = np.array(image)
    unknown_faces = face_recognition.face_encodings(pic)
    match_results = any(unknown_face for unknown_face in unknown_faces
                        if face_recognition.compare_faces([known_face], unknown_face))
    res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'".format(TOKEN, chat_id,
                                                                                               "ANI 0-5-2-5-3-8-1-6-4-8"
                                                                                               if match_results else "MI ZOT?!"))
    return Response("success")


if __name__ == '__main__':
    app.run(port=5002)

    # biden_encoding = face_recognition.face_encodings(known_image)[0]
    # unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

    # results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
    # print(results)
