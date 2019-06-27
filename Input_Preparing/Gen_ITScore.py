import os
from ops.os_operation import mkdir
##can't use ITSCore for license issue, please email to me for details:wang3702@purdue.edu
#we modified the ITScore, but we can't release because of ITScore license issue
def Gen_ITScore(file_path):

    listtmp = os.listdir(file_path)
    list1=[]
    for item in listtmp:
        if item[:7] == 'complex':
            list1.append(item)

    pathitscore = os.path.join(os.getcwd(), 'ITScore')
    pathaim = file_path
    pathwork = pathaim
    dependencypath = os.path.join(pathitscore, 'potentials.dat')
    dependencyaimpath = os.path.join(pathwork, 'potentials.dat')
    os.system('cp ' + dependencypath + ' ' + dependencyaimpath)
    dependencypath = os.path.join(pathitscore, 'ITScorePro')
    dependencyaimpath = os.path.join(pathwork, 'ITScorePro')
    os.system('cp ' + dependencypath + ' ' + dependencyaimpath)
    dependencypath = os.path.join(pathitscore, 'commonpara.mod')
    dependencyaimpath = os.path.join(pathwork, 'commonpara.mod')
    os.system('cp ' + dependencypath + ' ' + dependencyaimpath)
    os.chdir(pathwork)
    os.system('chmod 777 *')
    countexe = 0
    length = len(list1)
    while countexe + 8 < length:
        os.system(
            './ITScorePro ' + list1[countexe] + ' ' + list1[countexe + 1] + ' ' + list1[countexe + 2] + ' ' + list1[
                countexe + 3] + ' ' + list1[countexe + 4] + ' ' + list1[countexe + 5] + ' ' + list1[
                countexe + 6] + ' ' + list1[countexe + 7] + ' ')
        countexe += 8
    while countexe < length:
        os.system('./ITScorePro ' + list1[countexe])
        countexe += 1

