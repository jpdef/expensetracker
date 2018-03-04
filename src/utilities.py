
def print_loading(message,iteration):
    lchars = ['|','/','-','\\']
    str = "{} [{}]".format(message,lchars[iteration%len(lchars)])
    print(str, end="\r",flush=True)

def merge_dicts(x,y):
    z = x.copy()
    z.update(y)
    return z


if __name__ == "__main__":
    for i in range(0,100000):
        print_loading("Counting",i)
