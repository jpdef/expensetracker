
def print_loading(message,iteration):
    lchars = ['|','/','-','\\']
    str = "{} [{}]".format(message,lchars[iteration%len(lchars)])
    print(str, end="\r",flush=True)



if __name__ == "__main__":
    for i in range(0,100000):
        print_loading("Counting",i)
