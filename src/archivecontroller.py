import src.dbmanager as dbmanager
import os

from flask import Flask
from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import g

scribe = Blueprint('scribe', __name__,
                        template_folder='../templates')

"""
Dispatch Functions
"""


"""
archives() 
    valuess archives in database
"""
@scribe.route("/archives")
def archives():
    dbman = get_dbman()
    archives = dbman.get_tables()
    urls = [url_for('scribe.archive',name = a) for a in archives]
    items = list(zip(urls,archives))
    items.append (tuple([url_for('scribe.add_archive'),'Add archive']))
    return render_template('options.html',options=items,title="Archives")


"""
add_archive() 
    Adds additional archives 
"""
@scribe.route("/archives/add",methods=['POST','GET'])
def add_archive():
    dbman = get_dbman()
    if request.method=='POST':
        name = request.form['name']
        dbman.create_table(name,[{'name': "id", 'type': 'int', 'constraint' : ""}])
        return redirect(url_for('scribe.archives'))
    elif request.method == 'GET':
        return render_template('form.html',options=['name'],
                                           actions=url_for('scribe.add_archive'))
"""
archive(name)
    Returns archive webpage with name
    @param name : name of archive
"""
@scribe.route("/archives/<name>",methods=['GET'])
def archive(name):
    dbman = get_dbman()
    columns = dbman.get_columns(name)
    items = [ (tuple([url_for('scribe.add_row',name=name),'Add row'])),
              (tuple([url_for('scribe.add_column',name=name),'Add column']))]
    page_view = render_template('actions.html', options=items,title=name)
    
    rows = dbman.get_all(name)
    if rows:
        rows = rows[-5:]
        page_view += render_template('table.html',table=rows)
    
    return page_view
"""
most_freq()
    Returns most frequent element
"""
def most_freq(values):
    print("most frequent of",values)
    reduced = list(set(values))
    cnts = [0] * len(reduced)
    print(cnts)
    for elem in values:
        cnts[reduced.index(elem)] += 1
    max_cnt = max(cnts)
    if max_cnt > 0:
        try:
           return values[cnts.index(max(cnts))] or None
        except ValueError:
            return None

"""
classify()
    Classifies any empty input,based on other inputs
"""
def classify(name,other_inputs,column,dbman):
    knowns = []
    print('classify',column)
    for k,v in other_inputs.items():
        query_item = {}
        query_item[k]=v
        knowns += [v[column] for v in dbman.get(name,query_item) if v]
    return most_freq(knowns)

"""
autogenerate(name,form)
    fills out empty form input from inferences of filled in
    input
"""
def autogenerate(name,form,dbman):
    empty_inputs = {k for k,v in form.items() if not v }
    not_empty_inputs = {k:v for k,v in form.items() if  v}
    print("empty",empty_inputs)
    print("not empty",not_empty_inputs)
    for ei in empty_inputs:
        form[ei] = classify(name,not_empty_inputs,ei,dbman)
    return form

"""
add_row(name)
    Adds a column to the archive's table
    @param name : name of archive
"""
@scribe.route("/archives/<name>/add", methods=['GET','POST'])
def add_row(name):
    dbman = get_dbman()
    columns = dbman.get_columns(name)
    if request.method=='POST':
        form = request.form.to_dict(flat=True)
        print(form)
        if form['Autogenerate']:
            del form['Autogenerate']
            form = autogenerate(name,form,dbman)
            dbman.insert(name,form)
        else:
            del form['Autogenerate']
            dbman.insert(name,form)
        return redirect(url_for('scribe.archive',name=name))
    elif request.method == 'GET':
        # send the form data to user
        return render_template('autoform.html',options=columns,
                                           action=url_for('scribe.add_row',name=name))


"""
delete_row(name, id)
    Deletes a row from archive's table
    @param name : name of archive
    @param id   : row id
"""
@scribe.route("/archives/<name>/delete/<id>", methods=['POST'])
def delete_row(name, id):
    dbman = get_dbman()
    dbman.delete(name,{'id':id})
    return redirect(url_for('scribe.archives',name=name))

"""
add_column(name)
    Adds a column to the archive's table
    @param name : name of archive
"""
@scribe.route("/archives/<name>/mod", methods=['GET','POST'])
def add_column(name):
    dbman = get_dbman()
    if request.method=='POST':
        dbman.add_column(name, request.form)
        return redirect(url_for('scribe.archive',name=name))
    elif request.method == 'GET':
        return render_template('form.html',options=['name','type','contraint'],
                                           action=url_for('scribe.add_column',name=name))
"""
Utility functions
"""

def get_dbman():
    if not hasattr(g, 'dbman'):
        g.dbman = dbmanager.DBManager()
    return g.dbman