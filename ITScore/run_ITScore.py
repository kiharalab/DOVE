import os
from ops.os_operation import mkdir
def check_ITScore(item1):
    goapdecoys=os.path.join(os.getcwd(),"itscoredecoy")
    tempdir=os.path.join(goapdecoys,item1)
    if os.path.exists(tempdir):
        listfiles=os.listdir(tempdir)
        if len(listfiles)>20000:
            print('%s already generated'%item1)
            return False
    return True
def run_ITScore(item):
    pathdecoy=os.path.join(os.getcwd(),'decoys')
    pathitscore=os.path.join(os.getcwd(),'ITScore')
    pathaim=os.path.join(os.getcwd(),'itscoredecoy')
    pathwork=os.path.join(pathdecoy,item)
    pathmove=os.path.join(pathaim,item)
    mkdir(pathmove)
    listfiles=os.listdir(pathwork)
    list1=[]
    for item1 in listfiles:
        if item1[0:7]=='complex':
            list1.append(item1)
    list1.sort()
    dependencypath=os.path.join(pathitscore,'potentials.dat')
    dependencyaimpath=os.path.join(pathwork,'potentials.dat')
    os.system('cp '+dependencypath+' '+dependencyaimpath)
    dependencypath=os.path.join(pathitscore,'ITScorePro')
    dependencyaimpath=os.path.join(pathwork,'ITScorePro')
    os.system('cp '+dependencypath+' '+dependencyaimpath)
    dependencypath=os.path.join(pathitscore,'commonpara.mod')
    dependencyaimpath=os.path.join(pathwork,'commonpara.mod')
    os.system('cp '+dependencypath+' '+dependencyaimpath)
    os.chdir(pathwork)
    countexe=0
    length=len(list1)
    while countexe+8<length:
        os.system('./ITScorePro '+list1[countexe]+' '+list1[countexe+1]+' '+list1[countexe+2]+' '+list1[countexe+3]+' '+list1[countexe+4]+' '+list1[countexe+5]+' '+list1[countexe+6]+' '+list1[countexe+7]+' ')
        countexe+=8
    while countexe<length:
        os.system('./ITScorePro '+list1[countexe])
        countexe+=1
    listfiles=os.listdir(pathwork)

    for item1 in listfiles:
        if item1[-12:]=='_itscore.pdb':
            temppath=os.path.join(pathmove,item1)
            os.system('mv '+str(item1)+' '+temppath)



