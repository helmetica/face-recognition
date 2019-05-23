# -*- coding: utf-8 -*-

import os
import cv2
import time
import datetime
import multiprocessing
import face_recognition
import json
import base64
from flask import Flask, make_response, Response, request, render_template, redirect
from flask_cors import CORS

import db_helper

# configuration
DEBUG = True

COUNT_FRAME_WITH_DATA = 50
FRAME_HEIGHT = 120
FRAME_WIDTH = 160
FRAME_FPS = 30
TIME_DETECTION = 0.5 # обновлять время последней детекции каждые N мин

def StartWebServer(qI, port=5000):
    app = Flask(__name__)
    # app.config.from_object(__name__)

    # Flask-CORS нужен для отправки cross-origin-запросов (запросы, исходящие из другого протокола, IP-адреса, 
    # имени домена или порта), поэтому необходимо включить общий доступ к ресурсам (CORS).
    CORS(app)

    def eventStream():
        while True:
            result = qI.get()
            yield 'data: %s\n\n' % str(result)

    def getEvents():
        events = db_helper.get_events()
        return json.dumps(events, default=str)

    def getCameras():
        cameras = db_helper.get_cameras()
        return json.dumps(cameras, default=str)
    
    def getFaces():
        faces = db_helper.get_faces()
        return json.dumps(faces, default=str)

    @app.route("/events_data")
    def events_data():
        return Response(getEvents(), mimetype="text/event-stream")

    @app.route("/events_clear")
    def events_clear():
        db_helper.clear_events()
        return ''

    @app.route("/cameras_data")
    def cameras_data():
        return Response(getCameras(), mimetype="text/event-stream")

    @app.route("/faces_data")
    def faces_data():
        return Response(getFaces(), mimetype="text/event-stream")

    @app.route("/stream")
    def stream():
        return Response(eventStream(), mimetype="text/event-stream")

    @app.route("/")
    def index():
        return redirect("/events", code=302)

    @app.route("/events")
    def events():
        return render_template('events.html')

    @app.route("/cameras")
    def cameras():
        return render_template('cameras.html')

    @app.route("/faces")
    def faces():
        return render_template('faces.html')

    app.run("", port)
    app.debug = True

def CheckFace(cap, qI, camera, count_frame):
    i = 0
    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.imshow(camera['name'], img)
        if i % count_frame == 0:
            qI.put({'camera_name': camera['name'], 'camera_id': camera['id'], 'frame': img})
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        i += 1
    cap.release()
    cv2.destroyAllWindows()


def FullRecognizedFace(qI, qO):
    faces = db_helper.get_faces()

    print(faces)

    # Загружаем все знакомые лица
    known_face_encodings = []
    known_face_ids = []
    directory = os.getcwd() + '/'

    for face in faces:
        print(face['photo_path'])
        path_to_image = directory + face['photo_path']
        image = face_recognition.load_image_file(path_to_image)
        encoding = face_recognition.face_encodings(image)
        if len(encoding) > 0:
            face_encoding = encoding[0]
            known_face_encodings.append(face_encoding)
            known_face_ids.append(face['face_id'])

    i = 0
    while True:
        data_frame = qI.get()
        camera_name = data_frame.get('camera_name')
        camera_id = data_frame.get('camera_id')
        frame = data_frame.get('frame')
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            face_id = None

            if True in matches:
                first_match_index = matches.index(True)
                face_id = known_face_ids[first_match_index]
            
            # лицо определено
            if face_id is not None:
                face_info = db_helper.get_faces(face_id)[0]

                try:
                    img_data = open(face_info['photo_path'], 'rb' ).read()
                    img_data = "data:image/png;base64," + base64.b64encode(img_data).decode()
                except:
                    img_data = "data:image/jpeg;base64,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"

                time_detection = datetime.datetime.now()
                delta_time_detection = time_detection - face_info['last_detection']
                minutes_passed = delta_time_detection.seconds / 60

                print('compare last detec: ' + str(minutes_passed))

                if minutes_passed > TIME_DETECTION:
                    # обновить время последней детекции
                    db_helper.update_last_detection(face_info['face_id'], time_detection)

                    face_info['datetime'] = time_detection
                    face_info['camera'] = camera_name

                    new_person_j = json.dumps(face_info, default=str)
                    print(face_info['name'])

                    db_helper.insert_new_event(camera_id, face_info['face_id']) # брать камеры из БД

                    qO.put(new_person_j)
                else:
                    print('PASS')
            else:
                print('Unknown')
        i += 1

queueImg = multiprocessing.Queue()
queueToSend = multiprocessing.Queue()

detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
font = cv2.FONT_HERSHEY_SIMPLEX

# TODO: сделать получение камер из БД

cameras = db_helper.get_cameras()

# for c in cameras:
#     cam = cv2.VideoCapture(c['index'])
#     cam.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
#     cam.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
#     cam.set(cv2.CAP_PROP_FPS, FRAME_FPS)
#     prc = multiprocessing.Process(target=CheckFace, args=(cam, queueImg, c, COUNT_FRAME_WITH_DATA,))
#     prc.start()
#     print(c['name'])
#     print(prc.pid)

# запуск входной камеры
# entry_camera = cv2.VideoCapture(2)
# entry_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
# entry_camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
# entry_camera.set(cv2.CAP_PROP_FPS, FRAME_FPS)
# prc = multiprocessing.Process(target=CheckFace, args=(entry_camera, queueImg, 'Entry camera', COUNT_FRAME_WITH_DATA,))
# prc.start()
# print('cam1')
# print(prc.pid)

# запуск выходной камеры

# cam = {}
# cam['id'] = 1
# cam['name'] = 'Камера 1'
# exit_camera = cv2.VideoCapture(0)
# exit_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
# exit_camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
# exit_camera.set(cv2.CAP_PROP_FPS, FRAME_FPS)
# prc1 = multiprocessing.Process(target=CheckFace, args=(exit_camera, queueImg, cam, COUNT_FRAME_WITH_DATA,))
# prc1.start()
# print('cam2')
# print(prc1.pid)

# запуск сервера
prc2 = multiprocessing.Process(target=StartWebServer, args=(queueToSend, ))
prc2.start()
print(prc2.pid)

# FullRecognizedFace(queueImg, queueToSend)