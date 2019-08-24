import os
import numpy as np
import random
from ops.os_operation import mkdir
from Prediction.Build_Model import makecnn
from keras.callbacks import ModelCheckpoint
from keras.callbacks import EarlyStopping
from keras.callbacks import ReduceLROnPlateau
from Training.Keras_Loss import LossHistory
def Training(train_path,test_path,LR,Reg,batch_size):
    """
    :param train_path: training data dir
    :param LR: learning rate
    :param Reg: regularization term
    :return:
    a model
    """
    epoch_sample = int(np.ceil(len(trainlist) / batch_size))
    #1st step loading data
    #for here, because of my large amount training data, I used the list of numpy files instead of single one
    train_data_path=os.path.join(train_path, 'trainset.npy')
    aim_data_path=os.path.join(train_path,'aimset.npy')
    train_data=np.load(train_data_path)
    aim_data=np.load(aim_data_path)
    #loading validation data
    train_data_path = os.path.join(test_path, 'trainset.npy')
    aim_data_path = os.path.join(test_path, 'aimset.npy')
    prepare_val_label = False
    if os.path.exists(train_data_path) and os.path.exists(aim_data_path):
        prepare_val_label=True
        test_data = np.load(train_data_path)
        test_aim_data = np.load(aim_data_path)


    record_path=Generate_Logpath(LR,Reg)
    #specify the input channel

    channel = 4# please make a change if you want to add more channels
    model=makecnn(LR, Reg, 0.004,channel)
    hist_path = os.path.join(record_path, 'Training_Reg_' + str(Reg) + 'lr_' + str(LR) + '.jpg')
    #record the info during training
    history = LossHistory(hist_path, model, model_path)
    print(model.summary())
    random.seed(888)
    #shuffle data before training
    indexes=np.arange(len(train_data))
    random.shuffle(indexes)
    train_data=train_data[indexes]
    aim_data=aim_data[indexes]
    best_model_path = os.path.join(model_path, 'Bestlr_' + str(lr) + '_' + str(reg) + '.h5')#will automatically saved by the checkpointer
    #early stop setting to avoid overfitting
    # please adjust patience based on your experiments
    call_stop = EarlyStopping(monitor='val_loss', patience=4, verbose=1, mode='auto', restore_best_weights=True)
    checkpointer = ModelCheckpoint(filepath=best_model_path, verbose=1, save_best_only=True)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', patience=2, mode='auto')#adjust lr by the validation loss
    #you need to adjust patience based on your own features
    if prepare_val_label:
        # another choice, use your prepared data
        hist = model.fit(x=train_data, y=aim_data, batch_size=batch_size,
                     epochs=300, verbose=1, callbacks=[history, checkpointer, call_stop, reduce_lr],
                      validation_data=(test_data,test_aim_data),
                     shuffle=True, class_weight=None, sample_weight=None, initial_epoch=0,
                     steps_per_epoch=None, validation_steps=None, validation_freq=1)

    else:
        hist=model.fit(x=train_data, y=aim_data, batch_size=batch_size,
                   epochs=300, verbose=1, callbacks=[history, checkpointer, call_stop, reduce_lr],
                   validation_split=0.2, validation_data=None,
                   shuffle=True, class_weight=None, sample_weight=None, initial_epoch=0,
                   steps_per_epoch=None, validation_steps=None, validation_freq=1)
    history.loss_plot('batch')
    history.loss_plot('epoch')
    tmp_model_path = os.path.join(model_path, 'Finallr_' + str(LR) + 'epoch_' + str(300) + '.h5')
    model.save_weights(tmp_model_path)#save final model

    # if you are using training and validation list
    # hist = model.fit_generator(generate_arrays_from_file(trainlist, aimlist, batch_size),
    #                            steps_per_epoch=epoch_sample, epochs=300,
    #                            validation_data=generate_arrays_from_file(testlist, testaimlist, batch_size),
    #                            max_q_size=100, verbose=1, workers=4, use_multiprocessing=True,
    #                            callbacks=[history, checkpointer, call_stop, reduce_lr], validation_steps=100)


def Generate_Logpath(lr,reg):
    """
    :param lr: learning rate
    :param reg: regularization
    :return:
    the log path
    """
    record_path = os.path.join(os.getcwd(), 'Train_record')
    mkdir(record_path)
    record_path = os.path.join(record_path, 'lr_' + str(lr))
    mkdir(record_path)
    record_path = os.path.join(record_path, 'reg_' + str(reg))
    mkdir(record_path)
    return record_path