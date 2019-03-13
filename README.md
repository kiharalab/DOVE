# Dove_Pred
Dove Prediction Version
Dependency: tensorflow, keras, numpy
## General Instructions
 python main.py:   
  -h, --help            show this help message and exit   
  -F F                  decoy example path    
  --mode MODE, -M MODE  0: predicting for single docking model 1: predicting
                        and sorting for a list of docking models   
  --id ID               random id for the webserver notification, make sure
                        corresponding   
  --gpu GPU             Choose gpu id, example: '1,2'(specify use gpu 1 and 2)   

## 1 Predict single pdb file
python main.py --mode=0 -F [pdb_file] --id=888 --gpu=0   
if you need more than 1 gpu, use --gpu=0,1
## 2 Predict pdb file lists
python main.py --mode=1 -F [directory_path] --id=888 --gpu=0  
## Notice: All the docking models should use chain 'A' for receptors, use chain 'B' for ligands.
## Output record:
Output will be saved in the subdirectory of your models' directory.    
For mode 0,the output will be kept as file_name[:-4]_jobid[id].txt. For mode 1,the output will be kept as RECORD_jobid[id].txt
## Output format(Example):
complex.244440.pdb,0.80237,0.79943,0.90355,0.78516,-1.00000,-1.00000,0.91417,0.75000,     
(Explanation: first column is the file name, 2nd-9th column denotes the probability that model outputs, 2nd-ATOM20, 3rd-ATOM40 4th-GOAP 5th-ITScore 6th-ATOM+GOAP 7th-ATOM+ITScore 8th-GOAP+ITScore 9th-ATOM40+GOAP+ITScore. If it's -1, it means you do not have model weights files for corresponding deep learning model.)




