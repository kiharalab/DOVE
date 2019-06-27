from ops.os_operation import mkdir
import numpy as np
import os
from ops.Extract_Indicate import Indicate_to_channel
from Prediction.Build_Model import makecnn
import random
def Exec_Multi_Prediction(indicate,input_path):
    model_path=os.path.join(os.getcwd(),'Best_Model')
    model_path=os.path.join(model_path,indicate)
    model_path=os.path.join(model_path,'Best_Model.h5')
    if not os.path.exists(model_path):
        print('No model now')
        return None
    #load data
    inputdata_path = os.path.join(input_path, indicate + '.npy')
    if not os.path.exists(inputdata_path):
        print('No the evaluation input data or complex id info %s' % input_path)
        return None
    input_data = np.load(inputdata_path)
    # can't use anything related to ITSCore for license issue, please email to me for details:wang3702@purdue.edu
    if indicate=='itscore' or indicate=='atomitscore' or indicate=='goapitscore' or indicate=='atomgoapitscore':
        print('Because of ITScore license issue, we can not work on anything related to ITScore')
        print('*'*5+'Please contact me for details: wang3702@purdue.edu'+'*'*5)
        return [-1]*len(input_data)

    # First reload the model
    channel = Indicate_to_channel(indicate)
    model = makecnn(0, 0, 0, channel)
    model.load_weights(model_path)
    #Predict

    # Then applying the input to predict

    result=model.predict(input_data)
    result = result[:, 0]  # it outputs like (num_tested,1) format
    new_result=[]
    total_predlen=int(len(result)/4)
    for i in range(total_predlen):
        tmp_record =result[i*4:i*4+4]
        tmp_index = np.argsort(tmp_record)
        tmp_record = tmp_record[tmp_index]
        tmp_pred = tmp_record[0]
        new_result.append(tmp_pred)
    return new_result



