import os
def Get_Rcount(file_path):
    rcount=0
    with open(file_path, 'r') as file:
        line = file.readline()
        while line:
            if line[0:4] == 'ATOM' and line[21]=='A':
                rcount += 1
            line = file.readline()
    return rcount