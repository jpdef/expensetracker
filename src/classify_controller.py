from flask import Flask
from flask import render_template
from flask import request
from flask import g


"""
Creates a new classifcation 'object'
@param title   : name of classification
@param moment  : which of the columns will be used to classify the data
@param columns : list of dictionaries that defines each sql column for table
"""
@app.route("/classifcations/create/<title>",methods=['POST'])
def create_classification(title):
    # Entry should looks like:
    # {name : "Date"   , type : "varchar(255)", constraint : "", is_moment : "no" }
    # {name : "Amount" , type : "varchar(255)", constraint : "", is_moment : "yes" }

    categories = requests.form['categories'].split(' ')
    columns = requests.form['columns'].split(' ')
    newclass = Classifcation(title,columns=columns,categories=categories)

@app.route("/classifications/<title>",methods=['GET'])
def get_classification():
    newclass = Classifcation(title)

@app.route("/classification/<title>/column",methods=['GET'],['POST'])
def classifcation_column(title):
    pass

@app.route("/classifcations/<title>/classify",methods=['POST'])
def classify(title):
    newclass = Classification(title)
    ret = newclass.classify(requests.form['data'])


@app.route("/classifcations")
def list_classifcations():
    dbman = get_dbman()
    tables = dbman.get_tables()
    # Parse to the only get title names
    return set([t.spilt("_",1) , for t in tables)])
    
