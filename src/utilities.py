
def print_loading(message,iteration):
    lchars = ['|','/','-','\\']
    str = "{} [{}]".format(message,lchars[iteration%len(lchars)])
    print(str, end="\r",flush=True)

def merge_dicts(x,y):
    z = x.copy()
    z.update(y)
    return z

def list_dict_index(list_dict,key,value):
    for i,l in enumerate(list_dict):
        if l[key] == value:
            return i
    return -1

if __name__ == "__main__":
    for i in range(0,100000):
        print_loading("Counting",i)
