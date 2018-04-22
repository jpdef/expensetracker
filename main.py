from src import dbmanager
from src import archivecontroller

from datetime import datetime as dt
from flask import Flask
from flask import Blueprint
from flask import render_template
from flask import request
from flask import g
from flask import url_for
from flask import send_from_directory
app = Flask(__name__)

app.register_blueprint(archivecontroller.scribe,url_prefix='/scribe')

def get_dbman():
    if not hasattr(g, 'dbman'):
        g.dbman = dbmanager.DBManager()
    return g.dbman


@app.route('/')
def index():
    return render_template('welcome.html')

@app.route('/static/<path:path>')
def send_static(path):
	return send_from_directory('static',path)

if __name__ == '__main__':
    app.run()