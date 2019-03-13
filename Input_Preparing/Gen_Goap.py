import os
from ops.os_operation import mkdir
def Gen_GOAP(file_path):
    split_lists=os.path.split(file_path)
    pdb_id=split_lists[1]
    #Check if it has results, if it does,then do not run anymore
    listtmp=os.listdir(file_path)
    listrun=[]
    for item in listtmp:
        if item[:7]=='complex':
            listrun.append(item)
    goapset = os.path.join(os.getcwd(), 'Goap')
    pathgenerate = file_path
    os.chdir(goapset)
    # Copy files to the running directory
    os.system("cp fort.21_1.61_2 " + pathgenerate + "/fort.21_1.61_2")
    os.system("cp charge_inp.dat " + pathgenerate + "/charge_inp.dat")
    os.system("cp side_geometry.dat " + pathgenerate + "/side_geometry.dat")
    os.system("cp fort.31_g72_noshift5_new " + pathgenerate + "/fort.31_g72_noshift5_new")
    os.system("cp goap " + pathgenerate + "/goap")
    os.chdir(pathgenerate)
    if len(listrun)==0:
        print('no decoys avilable')
        return
    print('waiting dealing'+str(len(listrun)))
    os.system('chmod 777 *')
    file_object = open(str(pdb_id[0:4])+'.inp','w')
    try:
        file_object.write(goapset+'\n')
        for item2 in listrun:
            file_object.write(str(item2)+'\n')
    finally:
        file_object.close()
    os.system("./goap<"+str(pdb_id[0:4])+".inp")