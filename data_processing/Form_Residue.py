def Form_Residue(path):
    start=0
    line_count=0
    tmp_dict={}
    with open(path,'r') as file:
        line=file.readline()
        while line:
            line_count+=1
            if line[0:4]=='ATOM':
                residue_id=(line[21:27])
                if start==0:
                    tmp_residue_list=[]
                    pre_residue_id=residue_id
                if pre_residue_id!=residue_id:
                    tmp_dict[pre_residue_id]=tmp_residue_list
                    tmp_residue_list=[]
                    pre_residue_id=residue_id
                tmp_residue_list.append(start)
                start+=1#count lines,use line to find interface index

            line=file.readline()
    return tmp_dict

def Extract_Residue_Info(path):
    start = 0
    line_count = 0
    tmp_dict = {}
    with open(path, 'r') as file:
        line = file.readline()
        while line:
            line_count += 1
            if line[0:4] == 'ATOM':
                residue_id = (line[21:27])
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                if start == 0:
                    tmp_residue_list = []
                    pre_residue_id = residue_id
                if pre_residue_id != residue_id:
                    tmp_dict[pre_residue_id] = tmp_residue_list
                    tmp_residue_list = []
                    pre_residue_id = residue_id
                #atom_name=line[13:16]
                #atom_name=atom_name.strip()
                #if atom_name=='C' or atom_name=='CA' or atom_name=='N' or atom_name=='O':
                tmp_residue_list.append([x, y, z])
                start += 1  # count lines,use line to find interface index

            line = file.readline()
    return tmp_dict

def Extract_Residue_Incomplex(path,rcount):
    """

    :param path:
    :param rcount: residue number
    :return: the dict format of residues and ligands

    """
    rinfo={}
    linfo={}

    start=0
    with open(path,'r') as file:
        line=file.readline()

        while line:
            if line[0:4] == 'ATOM':
                residue_id = (line[21:27])
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                if start == 0:
                    tmp_residue_list = []
                    pre_residue_id = residue_id
                if pre_residue_id != residue_id:
                    if start<=rcount:
                        rinfo[pre_residue_id] = tmp_residue_list
                    else:
                        linfo[pre_residue_id] = tmp_residue_list
                    tmp_residue_list = []
                    pre_residue_id = residue_id
                #atom_name = line[13:16]
                #atom_name = atom_name.strip()
                #if atom_name == 'C' or atom_name == 'CA' or atom_name == 'N' or atom_name == 'O':
                tmp_residue_list.append([x, y, z])
                start += 1  # count lines,use line to find interface index

            line=file.readline()
    return rinfo,linfo