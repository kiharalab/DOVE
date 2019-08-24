from ops.os_operation import mkdir
import os
from data_processing.Get_Rcount import Get_Rcount
from data_processing.prepare_input import form_list,reform_input,Form_interface,form_atom_list
def Prepare_Data(file_path):
    """
    :param file_path: dir saves all the prepared data
    :return:
    the
    """
    #Create a dir to save the processed numpy files from the
    input_path = os.path.join(file_path, 'Training_Data')
    mkdir(input_path)
    save_path = input_path
    #considering you use corresponding name txt to record if it's an acceptable decoy or not
    pdb_file_list=[x for x in os.listdir(file_path) if 'pdb' in x]
    pdb_file_list.sort()
    aim_file_list = [x for x in os.listdir(file_path) if 'txt' in x]
    aim_file_list.sort()
    #here I just used atom40, the situation that information all you need comes from the pdb file
    #considering we do not need to use the modified goap and itscore, which requires the pdb name as complex.***.pdb
    atom40_input = []
    atom40_output=[]
    for start_index,file in enumerate(pdb_file_list):
        train_tmp_file=os.path.join(file_path,file)
        #process it
        if start_index==0:
            rcount = Get_Rcount(train_tmp_file)
        #get info for receptor and ligand
        #here info:[x_coordinate,y_coordinate,z_coordinate,atom_type]
        rlist, llist = form_atom_list(train_tmp_file, rcount)
        #get info in the interface area
        rlist, llist = Form_interface(rlist, llist, 0)  # This type doesn't matter
        #get the input from the info in interface area
        tempload, rlength, llength = reform_input(rlist, llist, 2)
        #here i used four rotation as an example
        atom40_tmp = tempload
        for k in range(4):
            atom40_input.append(atom40_tmp[:, :, :, :, k])
        #get the output
        aim_tmp_file=os.path.join(file_path,aim_file_list[start_index])
        with open(aim_tmp_file,'r') as tmp_file:
            line=tmp_file.readline()
            line=line.strip()
            aim_tmp=int(line)
        atom40_output.append(aim_tmp)
    #here you have two choices, saving them in separate numpy files or one file.
    #Considering your memory, if it's larger than 100GB, we strongly suggest to use one file as we do in our training
    atom40_input = np.array(atom40_input)
    atom40_output=np.array(atom40_output)
    train_path = os.path.join(save_path, 'trainset.npy')
    np.save(train_path, atom40_input)
    aim_path = os.path.join(save_path, 'aimset.npy')
    np.save(aim_path, atom40_output)
    return save_path

