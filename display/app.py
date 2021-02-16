#!/usr/bin/env python3

from flask import Flask, Response, request, abort, render_template, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

import requests
import random
import string
import subprocess
import os

app = Flask(__name__, static_url_path='/static')

# Log messages with Gunicorn
if not app.debug:
    import logging
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)

token = os.environ.get("TOKEN", "".join(random.choice(string.ascii_letters) for i in range(24)))
app.logger.info("Token: %s" % token)

cors_origins = '*'
if os.getenv('CORS_ALLOWED_ORIGINS'):
    cors_origins = os.getenv('CORS_ALLOWED_ORIGINS').split(',')
CORS(app, origins=cors_origins)

app.logger.info('CORS origins: %s', cors_origins)
socketio = SocketIO(app, cors_allowed_origins=cors_origins, path='/%s/socket.io' % token)

scripts_dir = os.path.join(os.path.dirname(__file__), "../scripts")
def run(script):
    s = subprocess.run([os.path.join(scripts_dir, script)], capture_output=True)
    return s.stdout.decode()

class Machine:
    def __init__(self, ip, name, token):
        self.ip = ip
        self.name = name
        self.token = token

    def __str__(self):
        return "%s (%s) (%s)" % (self.ip, self.name, self.token)

    def __repr__(self):
        return "Machine(%s)" % self

registered_machines = {}

def get_ips():
    return [i.ip for i in registered_machines.values()]

def get_ips_dict():
    return {i.ip: {"name": i.name} for i in registered_machines.values()}

@app.route('/<path:tok>/register', methods=['GET', 'POST'])
def register_route(tok):
    if tok != token:
        return abort(403)
    ip = request.args.get("ip") or request.form.get("ip")
    name = request.args.get("name") or request.form.get("name")
    ip_token = request.args.get("token") or request.form.get("token")

    registered_machines[ip] = Machine(ip, name, ip_token)
    print("Registered machine", registered_machines[ip])

    socketio.emit('update', {'ips': get_ips_dict()}, broadcast=True)

    return "added"

@app.route('/<path:tok>/unregister', methods=['GET', 'POST'])
def unregister_route(tok):
    if tok != token:
        return abort(403)
    ip = request.args.get("ip") or request.form.get("ip")

    if ip in registered_machines.keys():
        del registered_machines[ip]
        socketio.emit('update', {'ips': get_ips_dict()}, broadcast=True)

        return "removed"
    else:
        registered_machines.clear()
        socketio.emit('update', {'ips': get_ips_dict()}, broadcast=True)

        return "removed all"

@app.route('/<path:tok>/ips')
def ips_route(tok):
    if tok != token:
        return abort(403)
    return jsonify({"ips": get_ips_dict()})

@app.route('/<path:tok>')
def index_route(tok):
    if tok != token:
        return abort(403)
    return render_template("index.html")

@socketio.on('init')
def init_message(message):
    if message['tok'] != token:
        return
    print('init message:', message)

    emit('update', {'ips': get_ips_dict()})


ALLOWED_ACTIONS = ['status', 'audio/mute', 'audio/unmute', 'audio/toggle', 'video/off', 'video/on', 'video/toggle']

def run_action(ip, action):
    r = requests.post('http://%s:2626/%s' % (ip, action), data={'token': registered_machines[ip].token})
    print("run_action(%s): %s" % (r.status_code, r.text))
    if r.status_code == 200:
        return r.text
    return None

@socketio.on('command')
def command_message(message):
    if message['tok'] != token:
        return
    print('command message:', message)

    ip = message.get('ip')
    action = message.get('action')
    resp = None
    if action in ALLOWED_ACTIONS and ip in get_ips():
        resp = run_action(ip, action)

    emit('command_reply', {'response': resp, 'ip': ip, 'action': action})


if __name__ == '__main__':
    # app.run('0.0.0.0', port=2627)
    socketio.run(app, port=2627)