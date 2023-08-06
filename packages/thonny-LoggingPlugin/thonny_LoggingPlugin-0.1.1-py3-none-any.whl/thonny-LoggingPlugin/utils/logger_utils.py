def index_string_to_int(index):
    i = 0
    x = ''
    c = index[i]
    while c != '.' and i < len(index)-1: 
        x += c
        i+=1
        c = index[i]
    y = index[i+1:]

    return (int(x),int(y))

def indexs_on_same_line(index1,index2):
    return index_string_to_int(index1)[0] == index_string_to_int(index2)[0]

def indexs_on_same_column(index1,index2):
    return index_string_to_int(index1)[1] == index_string_to_int(index2)[1]

def getX(index):
    return index_string_to_int(index)[1]

def getY(index):
    return index_string_to_int(index)[0]

def create_index(x,y):
    return str(x)+'.'+str(y)