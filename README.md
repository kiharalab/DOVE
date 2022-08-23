# DOVE
[Protein Docking Model Evaluation by 3D Deep Convolutional Neural Networks](https://doi.org/10.1093/bioinformatics/btz870)
## Citation:
```
@article{wang2019protein,
  title={Protein Docking Model Evaluation by 3D Deep Convolutional Neural Networks},
  author={Wang, Xiao and Terashi, Genki and Christoffer, Charles W and Zhu, Mengmeng and Kihara, Daisuke},
  journal={Bioinformatics}
}
```
License: GPL v3. (If you are interested in a different license, for example, for commercial use, please contact us.) 
Contact: dkihara@purdue.edu

## Online platform: http://kiharalab.org/dove/
## What is Dove?
**Dove is a docking model evaluation method based on 3D deep convolutional neural networks.**  
(1) Dove is a protein docking model evaluation method, which distinguish good quality (acceptable quality in the CAPRI-criteria) from incorrect models. It is trained on around 2 million examples.    
(2) Compared to previous methods, it worked better on two different benchmark datasets, Zdock and Dockground.     
(3) In the cross-fold testing we conducted, we achieve around 85% accuracy on training set and around 70% accuracy on the validation set.  
**Network Architecture**
![](https://github.com/kiharalab/DOVE/blob/master/Web/img/model_bold.jpg)   
The network architecture of Dove. 100, 200, 200, 400, 400 are the number of filters in each layer. 20, 18, 16, 8, 6, 3 are the output cube size of each layer. Here our input size are 20*20*20. 10800, 1000, 100 denotes the number of neurons for fully connected layer. Block means that the data is a 3D cube, Flat is a 1D vector, Pool is a max-pooling, and FC is fully-connected network.
## Dove protocol
**Dove protocol consists of four steps:**   
(1) Dove computes and assigns GOAP and ITScore to each atom in a query docking model. GOAP and ITScore is knowledge-based potentials used in protein structure prediction.   
(2) As another type of input feature, Dove extracts the interface atom types and positions at the docking interface.   
(3) The query model is mapped on to a 3D grid, and GOAP, ITScore, and atom type information are mapped to each voxel. These are input features for the evaluation.   
(4) The deep learning trained model was applied to predict the the probability of the input model (decoy) being correct (an acceptable model with the CAPRI criteria). 1.0 is the highest score and 0.0 is the lowest. It applied 8 networks, each of which considers different features of the input decoys. Thus, Dove outputs 8 probability values.     
In the paper, the models were trained on a 4-fold cross validation. In this server, among the four models from the cross-validation, we implemented the model which gave the highest hit rate on the testing datasets.
![](https://github.com/kiharalab/DOVE/blob/master/Web/img/Flowchart.jpg)   
Notes: *ITScore is not made available in this released code because of the license issue.*

## Code Pre-required Library
```
Tensoflow: pip/conda install tensorflow==0.12
Keras: pip/conda install keras==2.2.4
Numpy: pip/conda install numpy
Matplotlib: pip/conda install matplotlib
```
## Usage
```
 python main.py:   
  -h, --help            show this help message and exit   
  -F F                  decoy example path    
  --mode MODE, -M MODE  0: predicting for single docking model 1: predicting
                        and sorting for a list of docking models   
  --id ID               random id for the webserver record to avoid the same file name with different contents
  --gpu GPU             Choose gpu id, example: '1,2'(specify use gpu 1 and 2)   
```
## 1 Predict single pdb file
```
python main.py --mode=0 -F [pdb_file] --id=888 --gpu=0   
```
if you need more than 1 gpu, use --gpu=0,1
## 2 Predict pdb file lists
```
python main.py --mode=1 -F [directory_path] --id=888 --gpu=0  
```
## 3 How to train a model  
```
python main.py --mode=2 -F [data_path] -F1 [validation_data_path] --gpu=0  --lr=0.1 --reg=1e-4 --batch_size=128
```
To help user add more features to train their own model for their purposes. I specifically added detailed comments in the main.py and other training codes in "Training" directory. If you have any questions regarding your training, please feel free to make contact with us.
### Notice: Receptor chain ID must be 'A', ligand chain ID must be 'B' (PDB format)    
### Output record:    
Output will be saved in the subdirectory of your models' directory.       
For mode 0,the output record will be kept as file_name[:-4]_jobid[id].txt.    
For mode 1,the output record will be kept as RECORD_jobid[id].txt
### Output format(Example):   
complex.244440.pdb,0.80237,0.79943,0.90355,0.78516,-1.00000,-1.00000,0.91417,0.75000,     
(Explanation: 1st column is the file name, 2nd-9th column denotes the probability of the decoy is correct (acceptable quality according to CAPRI). If the value is -1, it means the model is not evaluated using the corresponding features.)    
Note: *ITScore is not made available in this released code because of the license issue. Output that use ITScore in the feature combination is shown as -1.*

## Example: 
***Here is an example output of a correct decoy([link](https://github.com/kiharalab/DOVE/blob/master/Web/Example/Correct.pdb)):***   
![](https://github.com/kiharalab/DOVE/blob/master/Web/img/Correct.png)      
As you see in this example typically a correct decoy has a high probability (>0.5) from more than four feature combinations and no very small probability (< 0.01).    
Note: *ITScore is not made available in this released code because of the license issue. Output that use ITScore in the feature combination is shown as -1.*
      
***Here is an example output of an incorrect decoy([link](https://github.com/kiharalab/DOVE/blob/master/Web/Example/Incorrect.pdb)):***      
![](https://github.com/kiharalab/DOVE/blob/master/Web/img/Incorrect.png)  
Typically an incorrect decoy has at least one very small probability (< 0.01).    
Note: *ITScore is not made available in this released code because of the license issue. Output that use ITScore in the feature combination is shown as -1.*
     
***Explanation of different input features***   
![](https://github.com/kiharalab/DOVE/blob/master/Web/img/input_instruction.png) 

## Download Code
Limited by our 1GB quota size in github, our dependency files including model weights and Goap weight files can't save in the repo.
Here we offer two solustions to deal with the problem:
### 1. Download large files from our [server](http://kiharalab.org/github_data/DOVE_Large_File.tar.gz)
Then please use the following command to extract "Best_Model" and "Goap" directory and put them in under the repo's directory.
```
tar -xzvf DOVE_Large_File.tar.gz
```
### 2. (Suggested) Clone the repo from [Purdue github](https://github.itap.purdue.edu/kiharalab/DOVE)
```
git lfs clone https://github.itap.purdue.edu/kiharalab/DOVE
```
