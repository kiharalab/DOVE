import os
def Get_Rcount(file_path):
    """

    :param file_path: decoy path
    :return:
    the number of atoms in the receptor
    """
    #'A' chain and 'B' chain for receptor and ligand
    rcount=0
    with open(file_path, 'r') as file:
        line = file.readline()
        while line:
            if line[0:4] == 'ATOM' and line[21]=='A':
                rcount += 1
            line = file.readline()
    return rcount