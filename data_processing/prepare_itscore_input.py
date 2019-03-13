# -*- coding: utf-8 -*-
"""
Created on Dec 21, 1018

@author: wangxiao
"""
import os
import numpy as np

def form_itscore_list(item,rcount):
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
                itscore=float(line[62:70])

                atom_type = line[13:16].strip()
                residue_type=line[18:21]
                #First try CA distance of contact map


                if (goon):
                    if pre_residue_type == residue_type:
                        tmp_list.append([x, y, z,itscore,atom_type])
                    else:
                        llist.append(tmp_list)
                        tmp_list = []
                        tmp_list.append([x, y, z,itscore,atom_type])

                else:
                    if pre_residue_type == residue_type:
                        tmp_list.append([x, y, z,itscore,atom_type])
                    else:
                        rlist.append(tmp_list)
                        tmp_list = []
                        tmp_list.append([x, y, z,itscore,atom_type])

                atomid=int(dat_in[1])
                chainid=line[22]
                count=count+1
                pre_residue_type=residue_type
                pre_residue_id=residue_id
                pre_chain_id=chain_id
            line = file.readline()

    return rlist,llist