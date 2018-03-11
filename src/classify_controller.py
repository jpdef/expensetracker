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
@app.route("/classifcations/create/<title>")
def create_classification(title):
    # Get post data
    newclass = Classifcation(title,...)  
    # Return template with class information    

@app.route("/classifcations")
def list_classifcations():
    dbman = get_dbman()
    tables = dbman.get_tables()
    # Parse to the only get title names
    return set([t.spilt("_",1) , for t in tables)])
    
