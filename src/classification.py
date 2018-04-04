#!/usr/bin/env python
import src.dbmanager as dbmanager
import src.moments as moment
import src.utilities
import copy

class Classifcation:
    
    #Create a classifcation object
    def __init__(self, title,columns=[],categories=[]):
        self.title = title
        self.columns = columns
        self.dbman = dbmanager.DBManager()
        self.output_table = self.tablename("output")
        self.classification_table = self.tablename("meta")
        self.categories = categories if categories else self.get_categories()
        
        #Create moment objects or grab them from database
        moments = map( lambda x: x['name'], filter(lambda x : x['moment']=='yes',columns))
        self.moments = [moment.Moment(self,m) for m in moments] if moments else self.get_moments()
         
        if not self.tables_exist():
           self.make_tables()

    """
    Classifies a piece of unknown data
    """              
    def classify(self,entry):
        cat_weight = self.score(entry)
        weights = [x[1] for x in cat_weight]
        index = weights.index(max(weights))
        return cat_weight[index][0]

    """
    Makes sql tables for object perminance
    """
    def make_tables(self):
        #Create a table to hold classified output data
        columns = self.columns.append({"name":"category" , "type":"varchar(255)" , "constraint" : ""})
        self.dbman.create_table(self.output_table, self.columns)
 
        class_columns = [{"name":"category"   , "type":"varchar(255)" , "constraint" : ""},
         {"name":"sum_weight" , "type":"int"          , "constraint" : ""}]
        self.dbman.create_table(self.classification_table, class_columns)
        for c in self.categories:
            self.dbman.insert(self.classifcation_table,{"category" : c, "weight": 0})
   
    """
    Check if tables are in database
    """
    def tables_exist(self):
        tables = self.dbman.get_tables()
        return  ( self.output_table in tables and
                  self.classification_table in tables )
   
    """
    Score categories based on moments
    """
    def score(self,entry):
        cat_weight = []
        scores = [self.m.score(entry) for m in self.moments]
        for c in self.categories:
            #This adds all weights from specific category
            weight = reduce(lambda x,y : x+y,filter(lambda x : x == c, scores))
            cat_weight.append((c,weight))
    
    def get_categories(self):
        rows = self.dbman.get_all(self.classification_table)
        return [r['category'] for r in rows] if rows else []

    def get_moments(self):
        tables = self.dbman.get_tables()
        return filter(lambda x : self.title in x['name'] and 'moment' in x['name'], tables  )
 
    def tablename(self,label):
        return "%s_classify_%s" % (self.title,label)