from ops.os_operation import mkdir
import numpy as np
import os
from ops.Extract_Indicate import Indicate_to_channel
from Prediction.Build_Model import makecnn
import random
def Exec_Prediction(indicate,input_path):
    model_path=os.path.join(os.getcwd(),'Best_Model')
    model_path=os.path.join(model_path,indicate)
    model_path=os.path.join(model_path,'Best_Model.h5')
    if not os.path.exists(model_path):
        print('No model now')
        return -1
    # First reload the model
    channel = Indicate_to_channel(indicate)
    model = makecnn(0, 0, 0, channel)
    model.load_weights(model_path)
    #Predict
    inputdata_path = os.path.join(input_path, indicate + '.npy')
    if not os.path.exists(inputdata_path):
        print('No the evaluation input data or complex id info %s' % input_path)
        return -1
    # Then applying the input to predict
    input_data = np.load(inputdata_path)
    result=model.predict(input_data)
    result = result[:, 0]  # it outputs like (num_tested,1) format
    tmp_index = np.argsort(result)
    tmp_record = result[tmp_index]
    tmp_pred = np.mean(tmp_record[1:3])
    return tmp_pred



