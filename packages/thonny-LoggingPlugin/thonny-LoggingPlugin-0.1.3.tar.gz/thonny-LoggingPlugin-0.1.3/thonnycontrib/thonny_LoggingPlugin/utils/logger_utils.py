#little library with simples functions to simplify the main class code

#index are string coordinates like '1.5' or '15.1'
def index_string_to_int(index):
    """
    Return a tuple of the coordinates
    """
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
    """
    Return True if the index have the same first coordinate, False otherwise
    """
    return index_string_to_int(index1)[0] == index_string_to_int(index2)[0]

def indexs_on_same_column(index1,index2):
    """
    Return True if the index have the same second coordinate, False otherwise
    """
    return index_string_to_int(index1)[1] == index_string_to_int(index2)[1]

def getX(index):
    """
    return the second coordinate
    """
    return index_string_to_int(index)[1]

def getY(index):
    """
    return the first coordinate
    """
    return index_string_to_int(index)[0]

def create_index(x,y):
    """
    Return an str index made the 2 parameters
    """
    return str(x)+'.'+str(y)