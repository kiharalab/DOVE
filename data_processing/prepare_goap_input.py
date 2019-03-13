# -*- coding: utf-8 -*-
"""
Created on Dec 21, 1018

@author: wangxiao
"""
import os
import numpy as np

def form_goap_list(item,rcount):
    rlist=[]
    llist=[]
    #fout = open(item+'.iface', "w")
    with open(item,'r') as file:
        line = file.readline()               # call readline()
        while line[1:5]!='ATOM':
            line=file.readline()
        atomid=0
        count=1
        goon=False
        chainid=line[22]
        residue_type=line[18:21]
        pre_residue_type=residue_type
        tmp_list=[]
        pre_residue_id=0
        pre_chain_id=chainid
        while line:

            dat_in = line[0:80].split()
            if len(dat_in)==0:
                line=file.readline()
                continue

            if(dat_in[0]=='ATOM'):
                chain_id=line[22]
                residue_id=int(line[23:27])
                if (atomid > int(dat_in[1])):
                    if count <= rcount + 20 and count >= rcount - 20:
                        goon = True
                if residue_id < pre_residue_id:
                    if count <= rcount + 20 and count >= rcount - 20:
                        goon = True
                if pre_chain_id != chain_id:
                    if count <= rcount + 20 and count >= rcount - 20:
                        goon = True
                x = float(line[31:39])
                y = float(line[39:47])
                z = float(line[47:55])
                goap1=float(line[64:70])
                goap2=float(line[72:80])
                atom_type = line[13:16].strip()
                residue_type=line[18:21]
                #First try CA distance of contact map


                if (goon):
                    if pre_residue_type == residue_type:
                        tmp_list.append([x, y, z,goap1+goap2,atom_type])
                    else:
                        llist.append(tmp_list)
                        tmp_list = []
                        tmp_list.append([x, y, z,goap1+goap2,atom_type])

                else:
                    if pre_residue_type == residue_type:
                        tmp_list.append([x, y, z,goap1+goap2,atom_type])
                    else:
                        rlist.append(tmp_list)
                        tmp_list = []
                        tmp_list.append([x, y, z,goap1+goap2,atom_type])

                atomid=int(dat_in[1])
                chainid=line[22]
                count=count+1
                pre_residue_type=residue_type
                pre_residue_id=residue_id
                pre_chain_id=chain_id
            line = file.readline()
    print('in total, we have %d residues in receptor, %d residues in ligand' % (len(rlist), len(llist)))
    return rlist,llist

from data_processing.prepare_input import omitunnecessary
def reform_goap_input(rlist,llist,type):
    assert type==5 or type==6 or type==7 or type==8 or type==9 or type==10
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
    if type==5 or type==6 or type==9 or type==10:
        tempinput=np.zeros([20,20,20,1,4])
        tempinput=prepare_goap_part(rlist,llist,xmean,ymean,zmean,cut_off,tempinput,type)
    else:
        tempinput=np.zeros([20,20,20,5,4])##notice the first 4 denotes the 4 channels, which are 'C' 'N' 'O' 'Others', the final 4 denotes the rotation formed input data
        tempinput=prepare_atom_part(rlist,llist,rlist2,llist2,xmean,ymean,zmean,cut_off,tempinput)
        tempinput=prepare_goap_part(rlist,llist,xmean,ymean,zmean,cut_off,tempinput,type)
    #print('half cut %d, divide %d'%(half_cut,divide))


    return tempinput,rlength,llength

def prepare_atom_part(rlist,llist,r_atomlist,l_atomlist,xmean,ymean,zmean,cut_off,tempinput):
    count_use=0
    half_cut=int(cut_off/2)
    divide=1
    count_C=0
    count_N=0
    count_O=0
    count_other=0
    if half_cut==20:
        divide=2
        half_cut=10
    for i,item in enumerate(rlist):
        xo=int((float(item[0])-xmean)/divide)
        yo=int((float(item[1])-ymean)/divide)
        zo=int((float(item[2])-zmean)/divide)
        atom_type=r_atomlist[i]
        Status=True
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
    for i,item in enumerate(llist):
        xo=int((float(item[0])-xmean)/divide)
        yo=int((float(item[1])-ymean)/divide)
        zo=int((float(item[2])-zmean)/divide)
        Status=True
        atom_type=l_atomlist[i]
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
    print('C atom %d, N atom %d, O atom %d, other atom %d' % (count_C, count_N, count_O, count_other))
    return tempinput

def prepare_goap_part(rlist,llist,xmean,ymean,zmean,cut_off,tempinput,type):
    if type==5 or type==6 or type==9 or type==10:
        work_index=0
    else:
        work_index=4
    count_use=0
    half_cut=int(cut_off/2)
    divide=1
    if half_cut==20:
        divide=2
        half_cut=10
    #print (rlist[0])
    for i,item in enumerate(rlist):
        #print(item)
        #print(item[1])
        #print(item[2])
        #print(item[3])
        xo=int((float(item[0])-xmean)/divide)
        yo=int((float(item[1])-ymean)/divide)
        zo=int((float(item[2])-zmean)/divide)
        Status=True
        if xo<=-half_cut or xo>=half_cut or yo<=-half_cut or yo>=half_cut or zo<=-half_cut or zo>=half_cut:
            Status=False
        if Status:
            count_use+=1
            tempinput[xo+half_cut,yo+half_cut,zo+half_cut,work_index,0]=item[3]
            tempinput[-xo+half_cut,-yo+half_cut,zo+half_cut,work_index,1]=item[3]
            tempinput[-yo+half_cut,xo+half_cut,zo+half_cut,work_index,2]=item[3]
            tempinput[yo+half_cut,-xo+half_cut,zo+half_cut,work_index,3]=item[3]

    for i,item in enumerate(llist):
        xo=int((float(item[0])-xmean)/divide)
        yo=int((float(item[1])-ymean)/divide)
        zo=int((float(item[2])-zmean)/divide)
        Status=True
        if xo<=-half_cut or xo>=half_cut or yo<=-half_cut or yo>=half_cut or zo<=-half_cut or zo>=half_cut:
            Status=False
        if Status:
            count_use+=1
            tempinput[xo+half_cut,yo+half_cut,zo+half_cut,work_index,0]=item[3]
            tempinput[-xo+half_cut,-yo+half_cut,zo+half_cut,work_index,1]=item[3]
            tempinput[-yo+half_cut,xo+half_cut,zo+half_cut,work_index,2]=item[3]
            tempinput[yo+half_cut,-xo+half_cut,zo+half_cut,work_index,3]=item[3]

    print('%d atoms actually used in this example goap part'%count_use)
    return tempinput