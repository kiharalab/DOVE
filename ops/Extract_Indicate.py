def Indicate_to_channel(indicate):
    if indicate=='atom20' or indicate=='atom40':
        channel=4
    elif indicate=='atomgoap' or indicate=='atomitscore':
        channel=5
    elif indicate=='goapitscore':
        channel=2
    elif indicate=='atomgoapitscore':
        channel=6
    elif indicate=='goap' or indicate=='itscore':
        channel=1
    return channel

def Type_to_indicate(type):
    if type == 0:
        indicate = 'atom20'
    elif type == 1:
        indicate = 'atom40'
    elif type == 2:
        indicate = 'goap'
    elif type == 3:
        indicate = 'itscore'
    elif type == 4:
        indicate = 'atomgoap'
    elif type == 5:
        indicate = 'atomitscore'
    elif type == 6:
        indicate = 'goapitscore'
    elif type == 7:
        indicate = 'atomgoapitscore'
    return indicate