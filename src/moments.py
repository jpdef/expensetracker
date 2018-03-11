class Moment:
    """
    Either creates a new moment, or grabs one from db
    """
    def __init__(classification,moment_title,moment_parser=lambda x: x):     
        #Create a table to hold classification moment data
        self.moment_title = moment.title
        column = classifcation.columns[ list_dict_index(classfication.columns,'name',moment_title ) ]
        if not table_exists:
            dbman.create_table(self.moment_title,
                                    [{"name":"category"  , "type":"varchar(255)" , "constraint" : ""},
                                     {"name":"weight"    , "type":"int"          , "constraint" : ""},
                                     column]
                                    )    

    """
    Check if table is in database
    """
    def table_exists(self):
        tables = dbman.get_tables()
        return  self.moment_title in tables

    """
    Scores an entry if it matches any category. It returns
    the weight for that category
    """
    def score(entry):
        rows = dbman.get(entry)
        return [(r['category'],r['weight']) for r in rows]