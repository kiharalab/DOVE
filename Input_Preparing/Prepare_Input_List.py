from ops.os_operation import mkdir
import os
from Input_Preparing.Gen_Goap import Gen_GOAP
from Input_Preparing.Gen_ITScore import Gen_ITScore
from data_processing.prepare_input import form_list,reform_input,Form_interface,form_atom_list
from data_processing.prepare_goap_input import form_goap_list,reform_goap_input
from data_processing.prepare_itscore_input import form_itscore_list
from data_processing.Get_Rcount import Get_Rcount
import numpy as np
from ops.Write_List import Write_List
def Prepare_Input_List(file_path,random_id):

    input_path=os.path.join(file_path,'Dove'+str(random_id))
    mkdir(input_path)
    save_path = input_path
    #First copy to generate complex.id.txt
    listfiles=os.listdir(file_path)
    listfiles.sort()
    atom20_input = []
    atom40_input = []
    goap_input = []
    #itscore_input = []
    atomgoap_input = []
    #atomitscore_input = []
    #goapitscore_input = []
    #agi_input = []
    id_path = os.path.join(save_path, 'final_id.txt')
    if os.path.exists(id_path):
        return input_path
    final_id=[]
    id_list=[]
    for random_id,item in enumerate(listfiles):
        if item[-4:]!='.pdb':
            continue
        tmp_file_path=os.path.join(file_path,item)
        #first prepare goap and itscore for it.
        work_decoy1 = os.path.join(input_path, 'complex.' + str(random_id) + '.pdb')
        os.system('cp '+tmp_file_path+' '+work_decoy1)
        final_id.append(item)
        id_list.append(random_id)
    #Write final id record
    Write_List(id_path,final_id)
    #Gen goap and itscore
    pathroot=os.getcwd()
    Gen_GOAP(input_path)
    os.chdir(pathroot)
    # can't use anything related to ITSCore for license issue, please email to me for details:wang3702@purdue.edu
    #Gen_ITScore(input_path)
    #os.chdir(pathroot)
    #Generate input for our next step
    listfiles=os.listdir(input_path)

    for start_index,random_id in enumerate(id_list):


        #first prepare goap and itscore for it.
        work_decoy1 = os.path.join(input_path, 'complex.' + str(random_id) + '.pdb')
        work_decoy2 = os.path.join(input_path, str(random_id) + '_goap.pdb')
        #work_decoy3 = os.path.join(input_path, str(random_id) + '_itscore.pdb')
        if start_index==0:
            rcount = Get_Rcount(work_decoy1)
        rlist, llist = form_atom_list(work_decoy1, rcount)
        rlist, llist = Form_interface(rlist, llist, 0)  # This type doesn't matter
        tempload, rlength, llength = reform_input(rlist, llist, 1)
        for k in range(4):
            atom20_input.append(tempload[:, :, :, :, k])
        # Here, we only use the no rotation input
        tempload, rlength, llength = reform_input(rlist, llist, 2)
        atom40_tmp = tempload
        for k in range(4):
            atom40_input.append(atom40_tmp[:, :, :, :, k])
        # Then get goap
        rlist, llist = form_goap_list(work_decoy2, rcount)
        rlist, llist = Form_interface(rlist, llist, 0)
        tempload, rlength, llength = reform_goap_input(rlist, llist, 5)
        goap_tmp = tempload
        for k in range(4):
            goap_input.append(goap_tmp[:, :, :, :, k])
        # Finally, get itscore
        # can't use anything related to ITSCore for license issue, please email to me for details:wang3702@purdue.edu
        #rlist, llist = form_itscore_list(work_decoy3, rcount)
        #rlist, llist = Form_interface(rlist, llist, 0)
        #tempload, rlength, llength = reform_goap_input(rlist, llist, 6)
        #itscore_tmp = tempload
        #for k in range(4):
        #    itscore_input.append(itscore_tmp[:, :, :, :, k])
        # Now combine them
        for k in range(4):
            atomgoap_tmp = np.zeros([20, 20, 20, 5])
            atomgoap_tmp[:, :, :, 0:4] = atom40_tmp[:, :, :, :, k]
            atomgoap_tmp[:, :, :, 4:5] = goap_tmp[:, :, :, :, k]
            atomgoap_input.append(atomgoap_tmp)
            # can't use anything related to ITSCore for license issue, please email to me for details:wang3702@purdue.edu
            #atomgoap_tmp[:, :, :, 4:5] = itscore_tmp[:, :, :, :, k]
            #atomitscore_input.append(atomgoap_tmp)

            # goapitscore_tmp = np.zeros([20, 20, 20, 2])
            # goapitscore_tmp[:, :, :, 0:1] = goap_tmp[:, :, :, :, k]
            # goapitscore_tmp[:, :, :, 1:2] = itscore_tmp[:, :, :, :, k]
            # goapitscore_input.append(goapitscore_tmp)
            #
            # atomgoapitscore_tmp = np.zeros([20, 20, 20, 6])
            # atomgoapitscore_tmp[:, :, :, 0:4] = atom40_tmp[:, :, :, :, k]
            # atomgoapitscore_tmp[:, :, :, 4:5] = goap_tmp[:, :, :, :, k]
            # atomgoapitscore_tmp[:, :, :, 5:6] = itscore_tmp[:, :, :, :, k]
            # agi_input.append(atomgoapitscore_tmp)
    #Save the result
    atom20_input = np.array(atom20_input)
    atom40_input = np.array(atom40_input)
    goap_input = np.array(goap_input)
    #itscore_input = np.array(itscore_input)
    atomgoap_input = np.array(atomgoap_input)
    #atomitscore_input = np.array(atomitscore_input)
    #goapitscore_input = np.array(goapitscore_input)
    #agi_input = np.array(agi_input)
    atom20_path = os.path.join(save_path, 'atom20.npy')
    np.save(atom20_path, atom20_input)
    atom40_path = os.path.join(save_path, 'atom40.npy')
    np.save(atom40_path, atom40_input)
    goap_path = os.path.join(save_path, 'goap.npy')
    np.save(goap_path, goap_input)
    #itscore_path = os.path.join(save_path, 'itscore.npy')
    #np.save(itscore_path, itscore_input)
    atomgoap_path = os.path.join(save_path, 'atomgoap.npy')
    np.save(atomgoap_path, atomgoap_input)
    #atomitscore_path = os.path.join(save_path, 'atomitscore.npy')
    #np.save(atomitscore_path, atomitscore_input)
    #goapitscore_path = os.path.join(save_path, 'goapitscore.npy')
    #np.save(goapitscore_path, goapitscore_input)
    #atomgoapitscore_path = os.path.join(save_path, 'atomgoapitscore.npy')
    #np.save(atomgoapitscore_path, agi_input)
    return input_path