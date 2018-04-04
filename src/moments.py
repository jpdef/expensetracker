import src.utilities as utils
class Moment:
    """
    Either creates a new moment, or grabs one from db
    """
    def __init__(self,classification,title,moment_parser=lambda x: x):     
        #Create a table to hold classification moment data
        self.title = title
        self.classification = classification
        index = utils.list_dict_index(classification.columns,'name',title )
        
        if not self.table_exists() and index >= 0:
            column = classification.columns[ index ]
            print(column)
            self.classification.dbman.create_table(self.tablename(),
                                    [{"name":"category"  , "type":"varchar(255)" , "constraint" : ""},
                                     {"name":"weight"    , "type":"int"          , "constraint" : ""},
                                     column]
                                    )    

    """
    Check if table is in database
    """
    def table_exists(self):
        tables = self.classification.dbman.get_tables()
        return  self.tablename() in tables

    """
    Scores an entry if it matches any category. It returns
    the weight for that category
    """
    def score(self, entry):
        rows = self.classification.dbman.get(entry)
        return [(r['category'],r['weight']) for r in rows]

    def tablename(self):
        return "%s_classify_moment_%s" % (self.classification.title,self.title)