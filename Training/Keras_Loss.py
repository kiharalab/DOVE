import keras
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import keras.backend as K
import numpy as np
class LossHistory(keras.callbacks.Callback):
    """
    Record the training details during the process
    """
    def __init__(self,datapath,model,model_path):
        self.save_path=datapath
        self.model_path=model_path
        self.model=model
        self.losses = {'batch': [], 'epoch': []}
        self.accuracy = {'batch': [], 'epoch': []}
        self.val_loss = {'batch': [], 'epoch': []}
        self.val_acc = {'batch': [], 'epoch': []}
    #def on_train_begin(self, logs={}):


    def on_batch_end(self, batch, logs={}):
        self.losses['batch'].append(logs.get('loss'))
        self.accuracy['batch'].append(logs.get('acc'))
        self.val_loss['batch'].append(logs.get('val_loss'))
        self.val_acc['batch'].append(logs.get('val_acc'))

    def on_epoch_end(self, batch, logs={}):
        self.losses['epoch'].append(logs.get('loss'))
        self.accuracy['epoch'].append(logs.get('acc'))
        self.val_loss['epoch'].append(logs.get('val_loss'))
        self.val_acc['epoch'].append(logs.get('val_acc'))
        self.loss_plot('batch')
        self.loss_plot('epoch')
        tmp_path=os.path.join(self.model_path,str(len(self.accuracy['epoch']))+'_epoch.h5')
        self.model.save_weights(tmp_path)
        lr=K.get_value(self.model.optimizer.lr)
        tmp_path = os.path.join(self.model_path, str(len(self.accuracy['epoch'])) + '_lr.txt')
        lr_result=np.zeros(1)
        lr_result[0]=lr
        np.savetxt(tmp_path,lr_result)
    def loss_plot(self, loss_type):
        iters = range(len(self.losses[loss_type]))
        #create figure
        plt.figure()

        # loss
        plt.plot(iters, self.losses[loss_type], 'g', label='train loss')
        plt.grid(True)  # grid true
        plt.xlabel(loss_type)
        plt.ylabel('Loss')  # add comment
        plt.legend(loc="upper right")  # lengend settings
        if loss_type == 'batch':
            plt.savefig(self.save_path)
        else:
            plt.savefig(self.save_path[:-4] + '_epoch_loss.jpg')
        plt.figure()

            # val_loss
        plt.plot(iters, self.val_loss[loss_type], 'k', label='val loss')
        plt.grid(True)#grid true
        plt.xlabel(loss_type)
        plt.ylabel('Val Loss')#add comment
        plt.legend(loc="upper right")#lengend settings
        #plt.show()
        if loss_type=='epoch':
            plt.savefig(self.save_path[:-4]+'_epoch_val_loss.jpg')
        plt.figure()
        # acc
        plt.plot(iters, self.accuracy[loss_type], 'r', label='train acc')  # plt.plot(x,y)
        # val_acc
        plt.plot(iters, self.val_acc[loss_type], 'b', label='val acc')
        plt.xlabel(loss_type)
        plt.ylabel('accuracy')  # add comment
        plt.grid(True)  # grid true
        plt.legend(loc="upper right")  # lengend settings
        # plt.show()
        if loss_type=='batch':
            plt.savefig(self.save_path[:-4]+'_accu.jpg')
        else:
            plt.savefig(self.save_path[:-4] + '_epoch_accu.jpg')