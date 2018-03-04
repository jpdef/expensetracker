from src import dbmanager

from datetime import datetime as dt
from flask import Flask
from flask import render_template
from flask import request
from flask import g
app = Flask(__name__)

def get_dbman():
    if not hasattr(g, 'dbman'):
        g.dbman = dbmanager.DBManager()
    return g.dbman


@app.route('/')
def index():
    return render_template('welcome.html',time=dt.now().strftime("%H:%M %D/%M/%Y"))

@app.route('/expenses')
def expenses():
    return render_template('expenses.html')

@app.route('/expenses/tables', methods=['POST','GET'])
def expenses_tables():
    if (request.method == 'GET'):
        dbman = get_dbman()
        ret = dbman.get_tables()
        return render_template('options.html',title='tables',options=ret)
    else:
        return render_template('error.html',error="Invalid Request")

@app.route('/expenses/table/<tablename>', methods=['POST','GET'])
def expenses_table(tablename=None):
    if (request.method == 'GET'):
        dbman = get_dbman()
        table = dbman.get_all(tablename)
        return render_template('table.html',title=tablename,table=table)
    else:
        return render_template('error.html',error="Invalid Request")


@app.route('/expenses/chart', methods=['POST','GET'])
def expenses_chart():
    if (request.method == 'GET'):
        return render_template('expense_chart.html',expense_data=ret)
    else:
        return render_template('error.html',error="Invalid Request")

@app.route('/expenses/enter', methods=['POST','GET'])
def expenses_enter():
	pass


if __name__ == '__main__':
    app.run()