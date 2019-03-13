import numpy as np
from data_processing.prepare_goap_input import prepare_atom_part,prepare_goap_part
def reform_atomgoap_input(rlist,llist,type):
    assert type==10
    #type 5:goap type 7:atom+goap

    cut_off=40

    rlist1 = []  # form new rlist,(atom coordinate list instead of previous list)
    llist1 = []
    rlist2 = []  # Form new list, (atom list includes all information)
    llist2 = []
    for rindex, item1 in enumerate(rlist):
        residue1_len = len(item1)
        for i in range(residue1_len):
            atom = item1[i]
            tmp_list = []
            for k in range(4):
                tmp_list.append(atom[k])
            rlist1.append(tmp_list)
            rlist2.append(atom[4])

    for lindex, item1 in enumerate(llist):
        residue1_len = len(item1)
        for i in range(residue1_len):
            atom = item1[i]
            tmp_list = []
            for k in range(4):
                tmp_list.append(atom[k])
            llist1.append(tmp_list)
            llist2.append(atom[4])
    print('in the interface 10A cut off, we have %d residue, %d atoms in the receptor' % (len(rlist), len(rlist1)))
    print('in the interface 10A cut off, we have %d residue, %d atoms in the ligand' % (len(llist), len(llist1)))
    rlist1 = np.array(rlist1)
    llist1 = np.array(llist1)

    rlist = rlist1
    llist = llist1
    # print(rlist.shape)
    coordinate = np.concatenate([rlist1, llist1])

    # xmaxdis=max(coordinate[:,0])-min(coordinate[:,0])
    # ymaxdis=max(coordinate[:,1])-min(coordinate[:,1])
    # zmaxdis=max(coordinate[:,2])-min(coordinate[:,2])
    # xmean=(max(coordinate[:,0])+min(coordinate[:,0]))/2
    # ymean=(max(coordinate[:,1])+min(coordinate[:,1]))/2
    # zmean=(max(coordinate[:,2])+min(coordinate[:,2]))/2
    # if(xmaxdis>=cut_off or ymaxdis>=cut_off or zmaxdis>=cut_off):
    #
    #     rlist,llist= omitunnecessary(rlist,llist,xmean,ymean,zmean,cut_off)
    #     rlist=np.array(rlist)
    #     llist=np.array(llist)
    #     coordinate=np.concatenate([rlist,llist])
    #     xmean=(max(coordinate[:,0])+min(coordinate[:,0]))/2
    #     ymean=(max(coordinate[:,1])+min(coordinate[:,1]))/2
    #     zmean=(max(coordinate[:,2])+min(coordinate[:,2]))/2
    xmean = np.mean(coordinate[:, 0])
    ymean = np.mean(coordinate[:, 1])
    zmean = np.mean(coordinate[:, 2])
    rlength=len(rlist)
    llength=len(llist)
    #print (rlist[0])
    print('after processing, we only remained %d atoms in receptor, %d atoms in ligand'%(rlength,llength))
    #print(rlist.shape)

    tempinput=np.zeros([20,20,20,5,4])##notice the first 4 denotes the 4 channels, which are 'C' 'N' 'O' 'Others', the final 4 denotes the rotation formed input data
    tempinput=prepare_atom_part(rlist,llist,rlist2,llist2,xmean,ymean,zmean,cut_off,tempinput)
    tempinput=prepare_goap_part(rlist,llist,xmean,ymean,zmean,cut_off,tempinput,type)
    #print('half cut %d, divide %d'%(half_cut,divide))


    return tempinput,rlength,llength