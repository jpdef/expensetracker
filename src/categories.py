#!/usr/bin/env python
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

WTHRESHOLD = 2 

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
    self.table = {}
    def __init__(self):
        self.dbman = dbmanager.DBManager("categories", [])
        saved_catgories = self.db_man.get_all()
        self.load_table(saved_categories)

    def load_table(self,



    #categorize(self,data)
    #param self
    #param list of dict 
    def categorize(self,data):
        for d in data:
            c = self.get(d["Description"]) 
            if c :
                self.add(c,d["Description"])
            else :
                c = self.prompt_user("What is this %s ? " % d["Description"] ) 
                self.add(c,d["Description"])

    def add(self,category,phrase):
        w_phrase = [w_string(x,0) for x in phrase.split(' ')]
        if category in self.table:
            print("merging")
            self._merge(category, w_phrase)
        else:
            self.table[category] =  w_phrase
        self._sort()

    def get(self,phrase):
        scores = [self._score(phrase,k) for k in self.table.keys()]
        if scores and  (max(scores) >= WTHRESHOLD ): 
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
        self.print()
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
               print ("collision")
               self.table[category][index].incr_w()
           except ValueError:
               self.table[category].append(ws)

    
#TODO implement a weighting function

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
