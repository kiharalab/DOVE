import os
def check_rid(data_path):
    listfiles=os.listdir(data_path)
    count=0
    for item in listfiles:
        label=False
        tmp_path=os.path.join(data_path,item)
        rpath1=os.path.join(tmp_path,'receptor.pdb')
        rpath2=os.path.join(tmp_path,item[0:4]+'_r_u.pdb.ms')
        lpath1 = os.path.join(tmp_path, 'ligand.pdb')
        lpath2 = os.path.join(tmp_path, item[0:4] + '_l_u.pdb.ms')
        with open(rpath1,'r') as file:
            line=file.readline()
            while line:
                if line[0:4]=='ATOM':
                    try:
                        rid=int(line[23:27])
                        print('id %d in %s bound receptor' % (rid,item))
                    except:
                        print('no id in %s bound receptor'%item)
                        label=True
                    break
                line=file.readline()
        with open(rpath2,'r') as file:
            line=file.readline()
            while line:
                if line[0:4]=='ATOM':
                    try:
                        rid=int(line[23:27])
                        print('id %d in %s unbound receptor' % (rid,item))
                    except:
                        print('no id in %s unbound receptor'%item)
                        label = True
                    break
                line=file.readline()

        with open(lpath1,'r') as file:
            line=file.readline()
            while line:
                if line[0:4]=='ATOM':
                    try:
                        rid=int(line[23:27])
                        print('id %d in %s bound ligand' % (rid,item))
                    except:
                        print('no id in %s bound ligand'%item)
                        label = True
                    break
                line=file.readline()
        with open(lpath2,'r') as file:
            line=file.readline()
            while line:
                if line[0:4]=='ATOM':
                    try:
                        rid=int(line[23:27])
                        print('id %d in %s unbound ligand' % (rid,item))
                    except:
                        print('no id in %s unbound ligand'%item)
                        label = True
                    break
                line=file.readline()
        if label:
            count+=1
    print('in total, we have %d decoys that do not have residue id'%count)
