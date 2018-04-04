from src import dbmanager
from src import archivecontroller

from datetime import datetime as dt
from flask import Flask
from flask import Blueprint
from flask import render_template
from flask import request
from flask import g
from flask import url_for
app = Flask(__name__)

app.register_blueprint(archivecontroller.scribe,url_prefix='/scribe')

def get_dbman():
    if not hasattr(g, 'dbman'):
        g.dbman = dbmanager.DBManager()
    return g.dbman


@app.route('/')
def index():
    return render_template('welcome.html')

if __name__ == '__main__':
    app.run()