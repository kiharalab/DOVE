# -*- coding: utf-8 -*-
"""
Created on Dec 21, 1018

@author: wangxiao
"""
import os
import numpy as np
from multiprocessing import Process
from multiprocessing import Pool
import sys
from ops.os_operation import mkdir
def form_list(item):
    rlist=[]
    llist=[]
    #fout = open(item+'.iface', "w")
    with open(item,'r') as file:
        line = file.readline()               # call readline()
        txt_lists=line.split(',')
        specify_receptor=int(txt_lists[1])
        line=file.readline()
        line=file.readline()
        atomid=0
        count=1
        goon=False
        chainid=line[21]
        residue_type=line[17:20]
        pre_residue_type=residue_type
        tmp_list=[]
        pre_residue_id=0
        pre_chain_id=line[21]
        while line:

            dat_in = line[0:80].split()
            if len(dat_in)==0:
                line=file.readline()
                continue

            if(dat_in[0]=='ATOM'):
                chain_id=line[21]
                residue_id=int(line[23:26])
                if(atomid>int(dat_in[1])):
                    if count>=specify_receptor-100 and count<=specify_receptor+100:
                       goon=True

                if residue_id<pre_residue_id:
                    if count>=specify_receptor-100 and count<=specify_receptor+100:
                       goon=True
                if pre_chain_id!=chain_id:
                    if count>=specify_receptor-100 and count<=specify_receptor+100:
                       goon=True
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                residue_type=line[17:20]
                #First try CA distance of contact map


                if(goon):
                    if pre_residue_type==residue_type:
                        tmp_list.append([x,y,z])
                    else:
                        llist.append(tmp_list)
                        tmp_list=[]
                        tmp_list.append([x, y, z])

                else:
                    if pre_residue_type==residue_type:
                        tmp_list.append([x,y,z])
                    else:
                        rlist.append(tmp_list)
                        tmp_list=[]
                        tmp_list.append([x, y, z])

                atomid=int(dat_in[1])
                chainid=line[21]
                count=count+1
                pre_residue_type=residue_type
                pre_residue_id=residue_id
                pre_chain_id=chain_id
            line = file.readline()

    return rlist,llist

def form_atom_list(item,rcount):
    """
    :param item: decoy path
    :param rcount: number of atoms in the receptor
    :return:
    receptor list, ligand list: which includes the info for receptor and ligand
    here is [x_coordinate,y_coordinate,z_coordinate,atom_type]
    """
    rlist=[]
    llist=[]
    #fout = open(item+'.iface', "w")
    with open(item,'r') as file:
        line = file.readline()               # call readline()
        while line[0:4]!='ATOM':
            line=file.readline()
        atomid=0
        count=1
        goon=False
        chainid=line[21]
        residue_type=line[17:20]
        pre_residue_type=residue_type
        tmp_list=[]
        pre_residue_id=0
        pre_chain_id=line[21]
        while line:

            dat_in = line[0:80].split()
            if len(dat_in)==0:
                line=file.readline()
                continue

            if(dat_in[0]=='ATOM'):
                chain_id=line[21]
                residue_id=int(line[23:26])
                if(atomid>int(dat_in[1])):
                    if count<=rcount+20 and count>=rcount-20:
                        goon=True
                if residue_id<pre_residue_id:
                    if count<=rcount+20 and count>=rcount-20:
                        goon=True
                if pre_chain_id!=chain_id:
                    if count<=rcount+20 and count>=rcount-20:
                        goon=True
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                residue_type=line[17:20]
                #First try CA distance of contact map
                atom_type=line[13:16].strip()

                if (goon):
                    if pre_residue_type == residue_type:
                        tmp_list.append([x, y, z,atom_type])
                    else:
                        llist.append(tmp_list)
                        tmp_list = []
                        tmp_list.append([x, y, z,atom_type])

                else:
                    if pre_residue_type == residue_type:
                        tmp_list.append([x, y, z,atom_type])
                    else:
                        rlist.append(tmp_list)
                        tmp_list = []
                        tmp_list.append([x, y, z,atom_type])

                atomid=int(dat_in[1])
                chainid=line[21]
                count=count+1
                pre_residue_type=residue_type
                pre_residue_id=residue_id
                pre_chain_id=chain_id
            line = file.readline()
    print('in total, we have %d residues in receptor, %d residues in ligand'%(len(rlist),len(llist)))
    return rlist,llist

def Form_interface(rlist,llist,type):
    """
    :param rlist: receptor info
    :param llist: ligand info
    :param type: no use
    :return:
    information in the interface area
    """
    #type=1:20A type=others:40A
    cut_off=10
    cut_off=cut_off**2
    r_index=[]
    l_index=[]
    for rindex,item1 in enumerate(rlist):
        for lindex,item2 in enumerate(llist):
            min_distance=1000000
            residue1_len=len(item1)
            residue2_len=len(item2)
            for m in range(residue1_len):
                atom1=item1[m]
                for n in range(residue2_len):
                    atom2=item2[n]
                    distance=0
                    for k in range(3):
                        distance+=(atom1[k]-atom2[k])**2
                    if distance<=min_distance:
                        min_distance=distance
            if min_distance<=cut_off:
                if rindex not in r_index:
                    r_index.append(rindex)
                if lindex not in l_index:
                    l_index.append(lindex)
    newrlist=[]
    for k in range(len(r_index)):
        newrlist.append(rlist[r_index[k]])
    newllist=[]
    for k in range(len(l_index)):
        newllist.append(llist[l_index[k]])
    return newrlist,newllist
def omitunnecessary(rlist,llist,xmean,ymean,zmean,cut_off):
    r_remove=[]
    l_remove=[]
    for rindex,item1 in enumerate(rlist):

        for lindex,item2 in enumerate(llist):
            if lindex in l_remove:
                continue
            if rindex in r_remove:
                break
            check_label=False
            for k in range(3):
                check=abs(item1[k]-item2[k])
                if check>cut_off:
                    check_label=True
            if check_label:
                distance1=abs(item1[0]-xmean)+abs(item1[1]-ymean)+abs(item1[2]-zmean)
                distance2=abs(item2[0]-xmean)+abs(item2[1]-ymean)+abs(item2[2]-zmean)
                if distance1>distance2:
                    r_remove.append(rindex)
                else:
                    l_remove.append(lindex)
    r_remove=set(r_remove)
    l_remove=set(l_remove)
    newrlist=[]
    for i in range(len(rlist)):
        if i in r_remove:
            continue
        newrlist.append(rlist[i])
    newllist=[]
    for i in range(len(llist)):
        if i in l_remove:
            continue
        newllist.append(llist[i])
    return newrlist,newllist

def reform_input(rlist,llist,type):
    """
    :param rlist: info in receptor
    :param llist: info in ligand
    :param type: specify the voxel size
    :return:
    a voxel which includes the information in the interface area
    here 4 channels for different atoms based on their locations
    """
    assert  type==1 or type==2
    if type==1:
        cut_off=20
    else:
        cut_off=40
    rlist1=[]#form new rlist,(atom coordinate list instead of previous list)
    llist1=[]
    rlist2=[]#Form new list, (atom list includes all information)
    llist2=[]
    for rindex,item1 in enumerate(rlist):
        residue1_len = len(item1)
        for i in range(residue1_len):
            atom=item1[i]
            tmp_list=[]
            for k in range(3):
                tmp_list.append(atom[k])
            rlist1.append(tmp_list)
            rlist2.append(atom[3])

    for lindex,item1 in enumerate(llist):
        residue1_len = len(item1)
        for i in range(residue1_len):
            atom=item1[i]
            tmp_list=[]
            for k in range(3):
                tmp_list.append(atom[k])
            llist1.append(tmp_list)
            llist2.append(atom[3])
    print('in the interface 10A cut off, we have %d residue, %d atoms in the receptor'%(len(rlist),len(rlist1)))
    print('in the interface 10A cut off, we have %d residue, %d atoms in the ligand' % (len(llist), len(llist1)))
    rlist1=np.array(rlist1)
    llist1=np.array(llist1)
    #print(rlist1[0])
    rlist=rlist1
    llist=llist1
    #print(rlist.shape)
    coordinate=np.concatenate([rlist1,llist1])

    #xmaxdis=max(coordinate[:,0])-min(coordinate[:,0])
    #ymaxdis=max(coordinate[:,1])-min(coordinate[:,1])
    #zmaxdis=max(coordinate[:,2])-min(coordinate[:,2])
    xmean=np.mean(coordinate[:,0])
    ymean=np.mean(coordinate[:,1])
    zmean=np.mean(coordinate[:,2])
    # if(xmaxdis>=cut_off or ymaxdis>=cut_off or zmaxdis>=cut_off):
    #
    #     rlist,llist= omitunnecessary(rlist,llist,xmean,ymean,zmean,cut_off)
    #     rlist=np.array(rlist)
    #     llist=np.array(llist)
    #     #print(rlist.shape)
    #     #print (llist.shape)
    #     coordinate=np.concatenate([rlist,llist])
    #     xmean=(max(coordinate[:,0])+min(coordinate[:,0]))/2
    #     ymean=(max(coordinate[:,1])+min(coordinate[:,1]))/2
    #     zmean=(max(coordinate[:,2])+min(coordinate[:,2]))/2
    rlength=len(rlist)
    llength=len(llist)
    print('after processing, we only remained %d atoms in receptor, %d atoms in ligand'%(rlength,llength))
    half_cut=int(cut_off/2)
    divide=1
    if half_cut==20:
        divide=2
        half_cut=10
    tempinput=np.zeros([20,20,20,4,4])##notice the first 4 denotes the 4 channels, which are 'C' 'N' 'O' 'Others', the final 4 denotes the rotation formed input data
    count_use=0
    count_C=0
    count_N=0
    count_O=0
    count_other=0
    #print('half cut %d, divide %d'%(half_cut,divide))
    for i,item in enumerate(rlist):
        xo=int((float(item[0])-xmean)/divide)
        yo=int((float(item[1])-ymean)/divide)
        zo=int((float(item[2])-zmean)/divide)
        Status=True
        atom_type=rlist2[i]
        if xo<=-half_cut or xo>=half_cut or yo<=-half_cut or yo>=half_cut or zo<=-half_cut or zo>=half_cut:
            Status=False
        if Status:
            count_use+=1
            if atom_type=='C' or atom_type=='CA':
                tempinput[xo+half_cut,yo+half_cut,zo+half_cut,0,0]=tempinput[xo+half_cut,yo+half_cut,zo+half_cut,0,0]+1
                tempinput[-xo+half_cut,-yo+half_cut,zo+half_cut,0,1]=tempinput[-xo+half_cut,-yo+half_cut,zo+half_cut,0,1]+1
                tempinput[-yo+half_cut,xo+half_cut,zo+half_cut,0,2]=tempinput[-yo+half_cut,xo+half_cut,zo+half_cut,0,2]+1
                tempinput[yo+half_cut,-xo+half_cut,zo+half_cut,0,3]=tempinput[yo+half_cut,-xo+half_cut,zo+half_cut,0,3]+1
                count_C+=1
            elif atom_type=='N':
                tempinput[xo+half_cut,yo+half_cut,zo+half_cut,1,0]=tempinput[xo+half_cut,yo+half_cut,zo+half_cut,1,0]+1
                tempinput[-xo+half_cut,-yo+half_cut,zo+half_cut,1,1]=tempinput[-xo+half_cut,-yo+half_cut,zo+half_cut,1,1]+1
                tempinput[-yo+half_cut,xo+half_cut,zo+half_cut,1,2]=tempinput[-yo+half_cut,xo+half_cut,zo+half_cut,1,2]+1
                tempinput[yo+half_cut,-xo+half_cut,zo+half_cut,1,3]=tempinput[yo+half_cut,-xo+half_cut,zo+half_cut,1,3]+1
                count_N+=1
            elif atom_type=='O':
                tempinput[xo+half_cut,yo+half_cut,zo+half_cut,2,0]=tempinput[xo+half_cut,yo+half_cut,zo+half_cut,2,0]+1
                tempinput[-xo+half_cut,-yo+half_cut,zo+half_cut,2,1]=tempinput[-xo+half_cut,-yo+half_cut,zo+half_cut,2,1]+1
                tempinput[-yo+half_cut,xo+half_cut,zo+half_cut,2,2]=tempinput[-yo+half_cut,xo+half_cut,zo+half_cut,2,2]+1
                tempinput[yo+half_cut,-xo+half_cut,zo+half_cut,2,3]=tempinput[yo+half_cut,-xo+half_cut,zo+half_cut,2,3]+1
                count_O+=1
            else:
                tempinput[xo+half_cut,yo+half_cut,zo+half_cut,3,0]=tempinput[xo+half_cut,yo+half_cut,zo+half_cut,3,0]+1
                tempinput[-xo+half_cut,-yo+half_cut,zo+half_cut,3,1]=tempinput[-xo+half_cut,-yo+half_cut,zo+half_cut,3,1]+1
                tempinput[-yo+half_cut,xo+half_cut,zo+half_cut,3,2]=tempinput[-yo+half_cut,xo+half_cut,zo+half_cut,3,2]+1
                tempinput[yo+half_cut,-xo+half_cut,zo+half_cut,3,3]=tempinput[yo+half_cut,-xo+half_cut,zo+half_cut,3,3]+1
                count_other+=1
    print('%d atoms actually used in this receptor' % count_use)
    for i,item in enumerate(llist):
        xo=int((float(item[0])-xmean)/divide)
        yo=int((float(item[1])-ymean)/divide)
        zo=int((float(item[2])-zmean)/divide)
        Status=True
        atom_type=llist[i]
        if xo<=-half_cut or xo>=half_cut or yo<=-half_cut or yo>=half_cut or zo<=-half_cut or zo>=half_cut:
            Status=False
        if Status:
            count_use+=1
            if atom_type=='C' or atom_type=='CA':
                tempinput[xo+half_cut,yo+half_cut,zo+half_cut,0,0]=tempinput[xo+half_cut,yo+half_cut,zo+half_cut,0,0]+1
                tempinput[-xo+half_cut,-yo+half_cut,zo+half_cut,0,1]=tempinput[-xo+half_cut,-yo+half_cut,zo+half_cut,0,1]+1
                tempinput[-yo+half_cut,xo+half_cut,zo+half_cut,0,2]=tempinput[-yo+half_cut,xo+half_cut,zo+half_cut,0,2]+1
                tempinput[yo+half_cut,-xo+half_cut,zo+half_cut,0,3]=tempinput[yo+half_cut,-xo+half_cut,zo+half_cut,0,3]+1
                count_C+=1
            elif atom_type=='N':
                tempinput[xo+half_cut,yo+half_cut,zo+half_cut,1,0]=tempinput[xo+half_cut,yo+half_cut,zo+half_cut,1,0]+1
                tempinput[-xo+half_cut,-yo+half_cut,zo+half_cut,1,1]=tempinput[-xo+half_cut,-yo+half_cut,zo+half_cut,1,1]+1
                tempinput[-yo+half_cut,xo+half_cut,zo+half_cut,1,2]=tempinput[-yo+half_cut,xo+half_cut,zo+half_cut,1,2]+1
                tempinput[yo+half_cut,-xo+half_cut,zo+half_cut,1,3]=tempinput[yo+half_cut,-xo+half_cut,zo+half_cut,1,3]+1
                count_N+=1
            elif atom_type=='O':
                tempinput[xo+half_cut,yo+half_cut,zo+half_cut,2,0]=tempinput[xo+half_cut,yo+half_cut,zo+half_cut,2,0]+1
                tempinput[-xo+half_cut,-yo+half_cut,zo+half_cut,2,1]=tempinput[-xo+half_cut,-yo+half_cut,zo+half_cut,2,1]+1
                tempinput[-yo+half_cut,xo+half_cut,zo+half_cut,2,2]=tempinput[-yo+half_cut,xo+half_cut,zo+half_cut,2,2]+1
                tempinput[yo+half_cut,-xo+half_cut,zo+half_cut,2,3]=tempinput[yo+half_cut,-xo+half_cut,zo+half_cut,2,3]+1
                count_O+=1
            else:
                tempinput[xo+half_cut,yo+half_cut,zo+half_cut,3,0]=tempinput[xo+half_cut,yo+half_cut,zo+half_cut,3,0]+1
                tempinput[-xo+half_cut,-yo+half_cut,zo+half_cut,3,1]=tempinput[-xo+half_cut,-yo+half_cut,zo+half_cut,3,1]+1
                tempinput[-yo+half_cut,xo+half_cut,zo+half_cut,3,2]=tempinput[-yo+half_cut,xo+half_cut,zo+half_cut,3,2]+1
                tempinput[yo+half_cut,-xo+half_cut,zo+half_cut,3,3]=tempinput[yo+half_cut,-xo+half_cut,zo+half_cut,3,3]+1
                count_other+=1
    print('%d atoms actually used in this example'%count_use)
    print('C atom %d, N atom %d, O atom %d, other atom %d'%(count_C,count_N,count_O,count_other))
    return tempinput,rlength,llength