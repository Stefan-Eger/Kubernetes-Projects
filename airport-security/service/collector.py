# Description:
# The service will return a different kind of responses as a showcase.
# If the "destination" field in the request body has a url, the request
# will be forwarded to that destination, and the response of the remote
# service will be returned as a response.

from flask import Flask, jsonify, request, redirect, abort, Response
import requests

app = Flask(__name__)

bind_to = {'hostname': "0.0.0.0", 'port': 80}

# Services of other Teams
IMAGE_ANALYSIS_SERVICE_URL = "http://image-analysis-service:80/frame"
FACE_RECOGNITION_SERVICE_URL = "http://face-recognition-service:80/frame"
SECTION_SERVICE_URL = "http://section-service:80/persons"
ALERT_SERVICE_URL = "http://alert-service:80/alerts"

# referencing own REST API
COLLECTOR_SERVICE_FRAME_URL = "http://collector-service:80/frame"
COLLECTOR_SERVICE_PERSONS_URL = "http://collector-service:80/persons"
COLLECTOR_SERVICE_KNOWN_PERSONS_URL = "http://collector-service:80/known-persons"



def success_msg():
    return jsonify({"status": "OK"})

def forward_known_persons_to_Alert(known_person_json):
    msg = {
        'timestamp': known_person_json['timestamp'],
        'section': known_person_json['section'],
        'event': known_person_json['event'],
        'known-persons': known_person_json['known-persons']
    }

    if 'image' in known_person_json:
        msg['image'] = known_person_json['image']

    if 'extra-info' in known_person_json:
        msg['extra-info'] = known_person_json['extra-info']

    try:
        res = requests.post(ALERT_SERVICE_URL, json=msg)
        return res.text
    except Exception as e:
        response_json = {"error": {"code": 403, "message": str(e), "status": "DENIED"}}
        return response_json

@app.route('/known-persons', methods=['POST'])
def post_known_persons():
    # noinspection PyInterpreter
    if request.method == 'POST':
        if request.is_json:
            alert_response = forward_known_persons_to_Alert(request.json)
            return jsonify(alert_response)
        else:
            return abort(400)

    return abort(403)


def forward_persons_to_Section(persons_json):
    msg = {
        'timestamp': persons_json['timestamp'],
        'section': persons_json['section'],
        'event': persons_json['event'],
        'persons': persons_json['persons']
    }
    if 'image' in persons_json:
        msg['image'] = persons_json['image']

    if 'extra-info' in persons_json:
        msg['extra-info'] = persons_json['extra-info']

    try:
        res = requests.post(SECTION_SERVICE_URL, json=msg)
        return res.text
    except Exception as e:
        response_json = {"error": {"code": 403, "message": str(e), "status": "DENIED"}}
        return response_json


@app.route('/persons', methods=['POST'])
def post_persons():
    if request.method == 'POST':
        if request.is_json:
            section_response = forward_persons_to_Section(request.json)
            return jsonify(section_response)
        else:
            return abort(400)

    return abort(403)


def forward_frame_to_Image_Analysis(frame_json):
    msg = {
        'timestamp': frame_json['timestamp'],
        'image': frame_json['image'],
        'section': frame_json['section'],
        'event': frame_json['event'],
        'destination': COLLECTOR_SERVICE_PERSONS_URL
    }
    if 'extra-info' in frame_json:
        msg['extra-info'] = frame_json['extra-info']

    try:
        res = requests.post(IMAGE_ANALYSIS_SERVICE_URL, json=msg)
        return res.text
    except Exception as e:
        response_json = {"error": {"code": 403, "message": str(e), "status": "DENIED"}}
        return response_json


def forward_frame_to_Face_Recognition(frame_json):
    msg = {
        'timestamp': frame_json['timestamp'],
        'image': frame_json['image'],
        'section': frame_json['section'],
        'event': frame_json['event'],
        'destination': COLLECTOR_SERVICE_KNOWN_PERSONS_URL
    }
    if 'extra-info' in frame_json:
        msg['extra-info'] = frame_json['extra-info']

    try:
        res = requests.post(FACE_RECOGNITION_SERVICE_URL, json=msg)
        return (res.text)
    except Exception as e:
        response_json = {"error": {"code": 403, "message": str(e), "status": "DENIED"}}
        return response_json


@app.route('/frame', methods=['POST'])
def post_frame():
    if request.method == 'POST':
        if request.is_json:
            image_analysis_response = forward_frame_to_Image_Analysis(request.json)
            face_recognition_response = forward_frame_to_Face_Recognition(request.json)
            return jsonify({"Image Analysis": image_analysis_response, "Face Recognition": face_recognition_response})

        else:
            return abort(400)

    return abort(403)


if __name__ == "__main__":
    app.run(host=bind_to['hostname'], port=int(bind_to['port']), debug=True)