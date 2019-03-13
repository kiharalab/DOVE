#
# Copyright (C) 2018 Xiao Wang
# Email:xiaowang20140001@gmail.com
#

import parser
import argparse

def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-F',type=str, required=True,help='decoy example path')#File path for our MAINMAST code
    parser.add_argument('--mode','-M',type=int,required=True,help='0: predicting for single docking model 1: predicting and sorting for a list of docking models')
    parser.add_argument('--id', type=int,default=888,
                        help='random id for the webserver notification, make sure corresponding')
    parser.add_argument('--gpu',type=str,default='0',help='Choose gpu id, example: \'1,2\'(specify use gpu 1 and 2)')
    #Dense points part parameters
    args = parser.parse_args()
    # try:
    #     import ray,socket
    #     rayinit()
    # except:
    #     print('ray need to be installed')#We do not need this since GAN can't be paralleled.
    params = vars(args)
    return params