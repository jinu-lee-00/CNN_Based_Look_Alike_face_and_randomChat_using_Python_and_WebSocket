from flask import Flask, jsonify, request, render_template, make_response, session, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
#from flask_ngrok import run_with_ngrok
from flask_cors import CORS
import os
from flask_socketio import SocketIO, send
from flaskext.mysql import MySQL

app = Flask(__name__)

app.secret_key = 'qwertyuiopzxcvbnm'

socketio = SocketIO(logger=True, engineio_logger=True)
socketio.init_app(app)

from model.chat import socketio_init
socketio_init(socketio)

from routes import bp as main_blueprint
app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    socketio.run(app, debug=True)