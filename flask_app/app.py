# -* coding: utf-8 *-
"""
:py:mod:`flask_app.app`
-----------------------
Main chat flask application
"""
# System imports
import logging

# Third-party imports
from flask import Flask, render_template, request, url_for
from flask_socketio import SocketIO, emit

# Local imports

LOGGER = logging.getLogger('socketio-chat')
app = Flask('socketio-chat')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@socketio.on('connect')
def on_connect():
    LOGGER.debug('Client connected with sid: %s', request.sid)
    emit('set_name', {'name': request.sid})
    emit('user_connected', {'name': request.sid}, broadcast=True)


@socketio.on('disconnect')
def on_disconnect():
    LOGGER.debug('Client dropped connection: %s', request.sid)
    emit('user_disconnected', {'name': request.sid}, broadcast=True)


@socketio.on('join')
def on_join(msg):
    LOGGER.debug(msg)


@socketio.on('send_message')
def on_new_message(msg):
    emit('new_message', {'user': request.sid, 'message': msg['message']}, broadcast=True)


@app.route('/', methods=['GET'])
def route_index():
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app, debug=True)
