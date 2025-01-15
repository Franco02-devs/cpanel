# personal/scripts.py

def getFirstWord(string):
    space=string.find(" ")
    if space!=-1:
        return (string[0:space]).lower()
    return string.lower()