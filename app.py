#!/usr/bin/env python3

from flask import Flask, Response, request, abort

import random
import string
import subprocess
import os

app = Flask(__name__)

scripts_dir = os.path.join(os.path.dirname(__file__), "scripts")

token = os.environ.get("TOKEN", "".join(random.choice(string.ascii_letters) for i in range(8)))
print("Token: %s" % token)

@app.before_request
def is_token_set():
    provided_token = request.args.get("token") or request.form.get("token")
    if provided_token != token:
        abort(403)

def run(script):
    s = subprocess.run([os.path.join(scripts_dir, script)], capture_output=True)
    return s.stdout.decode()

@app.route('/status', methods=['GET', 'POST'])
def status_route():
    return run("zoom_status.sh")

@app.route('/audio', methods=['GET', 'POST'])
def audio_route():
    return run("zoom_audio_status.sh")

@app.route('/audio/mute', methods=['GET', 'POST'])
def mute_route():
    return run("zoom_mute.sh")

@app.route('/audio/unmute', methods=['GET', 'POST'])
def unmute_route():
    return run("zoom_unmute.sh")

@app.route('/audio/toggle', methods=['GET', 'POST'])
def audio_toggle_route():
    return run("zoom_audio_toggle.sh")

@app.route('/video', methods=['GET', 'POST'])
def video_route():
    return run("zoom_video_status.sh")

@app.route('/video/off', methods=['GET', 'POST'])
def video_off_route():
    return run("zoom_video_off.sh")

@app.route('/video/on', methods=['GET', 'POST'])
def video_on_route():
    return run("zoom_video_on.sh")

@app.route('/video/toggle', methods=['GET', 'POST'])
def video_toggle_route():
    return run("zoom_video_toggle.sh")

if __name__ == '__main__':
    app.run('0.0.0.0', port=2626)