import os
def change_bound_chain(bound_path,unbound_path,save_path):
    chain_list=[]
    with open(unbound_path,'r') as file:
        line=file.readline()
        start=0
        while line:
            chain_id=line[21]
            if start==0:
                pre_chainid=chain_id
                chain_list.append(chain_id)
            if pre_chainid!=chain_id:
                chain_list.append(chain_id)
                pre_chainid=chain_id
            line=file.readline()
            start+=1
    choose_chain_id=0
    with open(save_path,'w') as file1:
        with open(bound_path,'r') as file:
            line = file.readline()
            start = 0
            while line:
                chain_id = line[21]
                if start == 0:
                    pre_chainid = chain_id
                if pre_chainid != chain_id:
                    choose_chain_id+=1
                    pre_chainid = chain_id
                newline=line[0:21]+chain_list[choose_chain_id]+line[22:]
                file1.write(newline)
                line = file.readline()
                start+=1

def change_unbound_chain(r_unbound_path, l_unbound_path, data_path,new_r_path,new_l_path,rcount):
    listfiles=os.listdir(data_path)
    for item in listfiles:
        if item[0:7]=='complex' and item[-4:]=='.pdb':
            complex_path=os.path.join(data_path,item)
            break
    chain_list = []
    with open(complex_path, 'r') as file:
        line = file.readline()
        start = 0
        while line:
            chain_id = line[21]
            if start == 0:
                pre_chainid = chain_id
                chain_list.append(chain_id)

            start+=1
            if pre_chainid != chain_id:
                chain_list.append(chain_id)
                pre_chainid = chain_id
            line = file.readline()
    #print(chain_list)
    choose_chain_id = 0
    with open(new_r_path, 'w') as file1:
        with open(r_unbound_path, 'r') as file:
            line = file.readline()
            start = 0
            while line:
                chain_id = line[21]
                if start == 0:
                    pre_chainid = chain_id
                if pre_chainid != chain_id:
                    choose_chain_id += 1
                    pre_chainid = chain_id
                newline = line[0:21] + chain_list[choose_chain_id] + line[22:]
                file1.write(newline)
                line = file.readline()
                start += 1
    choose_chain_id+=1
    #print(choose_chain_id)
    with open(new_l_path, 'w') as file1:
        with open(l_unbound_path, 'r') as file:
            line = file.readline()
            start = 0
            #print(chain_list[choose_chain_id])
            while line:
                chain_id = line[21]
                if start == 0:
                    pre_chainid = chain_id
                if pre_chainid != chain_id:
                    choose_chain_id += 1
                    pre_chainid = chain_id
                newline = line[0:21] + chain_list[choose_chain_id] + line[22:]
                file1.write(newline)
                line = file.readline()
                start += 1
