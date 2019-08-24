from ops.argparser import argparser
import os
from ops.os_operation import mkdir
from ops.Write_record import Write_record
import numpy as np
from ops.Extract_Indicate import Type_to_indicate
from Input_Preparing.Prepare_Input_Single import Prepare_Input_Singe
from Prediction.Exec_Prediction import Exec_Prediction
from Input_Preparing.Prepare_Input_List import Prepare_Input_List
from Prediction.Exec_Multi_Prediction import Exec_Multi_Prediction
def run_pred_single(file_path,random_id,choose):
    import tensorflow as tf
    import keras.backend as K
    os.environ["CUDA_VISIBLE_DEVICES"] = choose
    #First prepare input and save it to the dir 'pdb_id[:-4]+random_id'
    input_path=Prepare_Input_Singe(file_path,random_id)
    print('input preparing finished')
    record=[]
    split_lists=os.path.split(file_path)
    record.append(split_lists[1])
    for type in range(8):
        indicate = Type_to_indicate(type)
        result=Exec_Prediction(indicate,input_path)
        record.append(result)
    print(record)
    return record,input_path
def run_pred_list(file_path,choose):
    import tensorflow as tf
    import keras.backend as K
    os.environ["CUDA_VISIBLE_DEVICES"] = choose
    # First prepare input and save it to the dir 'pdb_id[:-4]+random_id'
    listfiles=os.listdir(file_path)
    input_path = Prepare_Input_List(file_path, random_id)
    print('input preparing finished')
    record = []
    for type in range(8):
        indicate = Type_to_indicate(type)
        result = Exec_Multi_Prediction(indicate, input_path)
        record.append(result)
    final_record=[]
    #First get file name
    id_path = os.path.join(input_path, 'final_id.txt')
    file_list=[]
    with open(id_path,'r') as file:
        line=file.readline()
        file_list=line.split(',')
        file_list=file_list[:-1]#emilinate the last "" record
    for count,item in enumerate(file_list):
        tmp_record=[]
        tmp_record.append(item)
        for record_item in record:
            if record_item!=None:
                tmp_record.append(record_item[count])
            else:
                tmp_record.append(-1)
        final_record.append(tmp_record)
    print(final_record)
    return final_record,input_path
if __name__ == "__main__":
    params = argparser()
    #print(params)
    if params['mode']==0:
        file_path=params['F']
        random_id=params['id']
        gpu_id=params['gpu']
        file_path=os.path.abspath(file_path)
        record,input_path=run_pred_single(file_path,random_id,gpu_id)
        split_lists=os.path.split(file_path)
        pdb_id=split_lists[1]
        Write_record([record], input_path,pdb_id[:-4] , random_id)
    elif params['mode']==1:
        file_path = params['F']
        random_id = params['id']
        gpu_id = params['gpu']
        file_path = os.path.abspath(file_path)
        final_record,input_path=run_pred_list(file_path,gpu_id)
        Write_record(final_record, input_path, 'RECORD', random_id)
    elif params['mode']==2:
        #specially for anyone want to extend the code for training their own code
        # 1. Prepare your own data
        #here let's use the DOVE as an Example
        #We need to have a list of pdb files in the same directory
        file_path=params['F']
        file_path = os.path.abspath(file_path)
        #then we generate training input and output for future training
        from Training.Prepare_Data import Prepare_Data
        train_path=Prepare_Data(file_path)

        file_path = params['F1']
        if file_path!=None:
            file_path = os.path.abspath(file_path)
            # then we generate training input and output for future validation
            from Training.Prepare_Data import Prepare_Data

            test_path = Prepare_Data(file_path)#for validation use
        else:
            test_path=os.getcwd()
        #2 specify gpu id, learning rate and
        choose = params['gpu']
        lr = params['lr']
        reg = params['reg']
        batch_size=params['batch_size']
        os.environ["CUDA_VISIBLE_DEVICES"] = choose
        import tensorflow as tf
        import keras.backend as K

        # gpu_fraction = 0.1
        # gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=gpu_fraction)
        config = tf.ConfigProto(allow_soft_placement=True)
        config.gpu_options.allow_growth = True  # allocate as you need
        session = tf.Session(config=config)
        K.set_session(session)
        #3 start training
        #also saved the model in a sub dir in the train path

        from Training.Training import Training
        model=Training(train_path,test_path,lr,reg,batch_size)



