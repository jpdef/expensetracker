#!/usr/bin/env python
import dbmanager
import utilities
import copy

class Classifcation:
    
    #Create a classifcation object
    def __init__(title,columns={},moments=[],categories=[]):
        self.output_table = "%s_classfiy_%s" % (title,"output")
        self.moments_tables = ["%s_classify_%s" % (title,m) for m in moments]
        self.classification_table = "%s_classify_%s" % (title,"meta")
        self.categories = categories
        
        #Create moment objects
        self.moments = [moment.Moment(self,m) for m in moments]
         
        if not self.tables_exist():
           self.make_table()

    """
    Classifies a piece of unknown data
    """              
    def classify(title, entry):
        cat_weight = self.score(entry)
        weights = [x[1] for x in cat_weight]
        index = weights.index(max(weights))
        return cat_weight[index][0]

    """
    Makes sql tables for object perminance
    """
    def make_table():
        #Create a table to hold classified output data
        self.columns += {"name":"category" , "type":"varchar(255)" , "constraint" : ""}
        dbman.create_table(self.output_table, columns)
   
    """
    Check if tables are in database
    """
    def tables_exist():
        tables = dbman.get_tables()
        return  ( self.output_table in tables and
                  self.classifcation_table in tables )
   
    """
    Score categories based on moments
    """
    def score(entry):
        cat_weight = []
        scores = [self.m.score(entry) for m in self.moments]
        for c in self.categories:
            #This adds all weights from specific category
            weight = reduce(lambda x,y : x+y,filter(lambda x : x == c, scores))
            cat_weight.append((c,weight))
    
    def make_tablename(title, label):
        return "%s_classification_%s" % (title,label)