from datetime import datetime as dt
from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('welcome.html',time=dt.now().strftime("%H:%M %D/%M/%Y"))

@app.route('/expenses')
def expenses():
    return render_template('expenses.html')

@app.route('/expenses/table', methods=['POST','GET'])
def expenses_table():
    if (request.method == GET):
	    ret = self.dbmanager.get_rows()
	    return render_template('expense_table.html',expense_data=ret)
	else:
        return render_template('error.html',error="Invalid Request")

@app.route('/expenses/chart', methods=['POST','GET'])
def expenses_chart():
	    if (request.method == GET):
	    ret = self.dbmanager.get_rows()
	    return render_template('expense_chart.html',expense_data=ret)
	else:
        return render_template('error.html',error="Invalid Request")

@app.route('/expenses/enter', methods=['POST','GET'])
def expenses_enter():
	pass