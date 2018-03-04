#!/usr/bin/env python
import dbmanager
import utilities
import copy
"""
Class w_string
     Is a weighted string based on confirmation of category
     --------------- 
    | normalized    |
    | weight/100    |
    |_______________|
    | "foo"         |
    |               |
     --------------- 
"""

WTHRESHOLD = 0 

class w_string:
      def __init__(self):
          self.string = ""
          self.weight = 0

      def __init__(self,s,w):
          self.string = s
          self.weight = w
      
      def __str__(self):
          return "[ {} , {} ]".format(self.string, self.weight)
      
      def __gt__(self,other):
          return other.weight < self.weight
      
      def __lt__(self,other):
          return not other.weight < self.weight

      def __eq__(self,other):
          return (self.string == other.string) and (self.weight == other.weight)

      def to_string(self):
          return self.string

      def to_weight(self):
          return self.weight
      
      def incr_w(self,w=1):
          self.weight += w

"""
Data Structure:
    table is a -> {"category key" : [w_string]} 
"""
class Categories :
    table = {}
    prev_table = {}
    change_table = {}
    hit = miss = 0.0
    def __init__(self):
        self.dbman = dbmanager.DBManager()
        self.dbman.create_table("categories",
                                [{"name":"category"  , "type":"varchar(255)" , "constraint" : ""},
                                 {"name":"desc"      , "type":"varchar(255)" , "constraint" : ""},
                                 {"name":"weight"    , "type":"int"          , "constraint" : ""}]
                                )
        saved_categories = self.dbman.get_all("categories")
        self.load_from_db(saved_categories)
        self._sort()
        self.prev_table = copy.deepcopy(self.table)
        for k in self.table.keys():
            self.change_table[k] = []   
        self.print()
   
    def __del__(self):
         if (self.hit + self.miss)  !=  0:
             print( "Sucess rate %" + str((self.hit/(self.hit +self.miss ))*100))
             self.load_to_db()
    
    #Loads saved categories into memory 
    def load_from_db(self,saved_categories):
        if saved_categories :
           for s in saved_categories:
               try:
                    ws = w_string(s["desc"],s["weight"])
                    self.table[ s["category"] ].append(ws)
               except KeyError:
                    self.table[ s["category"]] = []

    #Loads catgory table to database
    def load_to_db(self):
        self.diff_table()
        self.print() 
        print(self.change_table)
        for k,v in self.change_table.items():
            for i,w in enumerate(v):
                utilities.print_loading("Loading to db",i)
                self.dbman.insert("categories",{"category":k , "desc":w.string , "weight":w.weight},unique="weight")
   
    def diff_table(self):
        for k,v in self.table.items():
            if k not in self.prev_table:
                self.change_table[k] = self.table[k]
            else:
                print("{} {}".format(len(self.prev_table[k]),len(self.table[k])))
                for i,w in enumerate(v):
                    if i >= len(self.prev_table[k]):
                        print("exceed category list")
                        self.change_table[k].append(w)
                    elif (self.prev_table[k][i] != w):
                        self.change_table[k].append(w)
                        



    def categorize(self,unknown):
        c = self.get(unknown) 
        if c :
            self.hit += 1
            self.add(c,unknown)
        else :
            self.miss += 1
            c = self.prompt_user("What is this %s ? " % unknown ) 
            self.add(c,unknown)
        return c

    def add(self,category,phrase):
        w_phrase = [w_string(x,0) for x in phrase.split(' ')]
        if category in self.table:
            self._merge(category, w_phrase)
        else:
            self.table[category] =  w_phrase

    def get(self,phrase):
        scores = [self._score(phrase,k) for k in self.table.keys()]
        print("{} got scores {} for categories {}".format(phrase, scores,self.table.keys() )) 
        if scores and  (max(scores) > WTHRESHOLD ): 
            index = scores.index(max(scores))
            return list(self.table.keys())[index]
        else:
            return

    def print(self):
        for k,v in self.table.items():
            print("%s --> " %  k,end='')
            for ws in v:
                print (str(ws) ,end="-->")
            print(flush=True)
  
    def prompt_user(self,msg):
        resp = input(msg)
        return resp

    #Needs work
    def _score(self,phrase,category):
        score = 0 
        for p in  [x for x in phrase.split(' ')]:
            strings = [ws.to_string() for ws in self.table[category]]
            if p in strings:
               index = strings.index(p)
               score += self.table[category][index].to_weight()
            else:
               score = 0
        
        return score

    def _sort(self):
        for k,v in self.table.items():
            self.table[k] =  sorted(self.table[k],reverse=True)

    
    def _merge(self,category,w_phrase):
        ss = [ x.string for x in self.table[category]]
        for ws in w_phrase: 
           s = ws.string
           try :
               index = ss.index(s)
               self.table[category][index].incr_w()
           except ValueError:
               self.table[category].append(ws)

    

if __name__ == "__main__":
    #Execute tests on weight string object
    ws1 = w_string("foo",0)
    ws2 = w_string("bar",1)
    print ( str(ws1), str(ws2) )
    #Execute Tests on categories object
    ctgs = Categories()
    ctgs.add("foo", "this is a phrase")
    ctgs.add("foo", "phrase")
    ctgs.add("bar", "this is also a phrase")
    ctgs.add("bar", "this is a different phrase")
    ctgs.print()
    
    #Test Categorize
    ss = "phrase also"
    print("Categorize %s" % ss )
    print(ctgs.get(ss))
    
    ss = "this"
    print("Categorize %s" % ss )
    print(ctgs.get(ss))
    ctgs.load_to_db()
