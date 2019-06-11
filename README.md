# Dove_Pred
## Reference:
Docking Model Evaluation by 3D Deep Convo-lutional Neural Networks Xiao Wang, Genki Terashi, Charles W. Christoffer, Mengmeng Zhu, and Daisuke Kihara, In submission (2019) 
## Online platform: http://kiharalab.org/dove/
## What is Dove?
**Dove is a docking model evaluation method based on 3D deep convolutional neural networks.**  
(1) Dove is a protein docking model evaluation method, which distinguish good quality (acceptable quality in the CAPRI-criteria) from incorrect models. It is trained on around 2 million examples.    
(2) Compared to previous methods, it worked better on two different benchmark datasets, Zdock and Dockground.     
(3) In the cross-fold testing we conducted, we achieve around 85% accuracy on training set and around 70% accuracy on the validation set.  
**Network Architecture**
![](https://github.com/kiharalab/Dove_Pred/blob/master/Web/img/model_bold.jpg)   
The network architecture of Dove. 100, 200, 200, 400, 400 are the number of filters in each layer. 20, 18, 16, 8, 6, 3 are the output cube size of each layer. Here our input size are 20*20*20. 10800, 1000, 100 denotes the number of neurons for fully connected layer. Block means that the data is a 3D cube, Flat is a 1D vector, Pool is a max-pooling, and FC is fully-connected network.
## Dove protocol
**Dove protocol consists of four steps:**   
(1) Dove computes and assigns GOAP and ITScore to each atom in a query docking model. GOAP and ITScore is knowledge-based potentials used in protein structure prediction.   
(2) As another type of input feature, Dove extracts the interface atom types and positions at the docking interface.   
(3) The query model is mapped on to a 3D grid, and GOAP, ITScore, and atom type information are mapped to each voxel. These are input features for the evaluation.   
(4) The deep learning trained model was applied to predict the the probability of the input model (decoy) being correct (an acceptable model with the CAPRI criteria). 1.0 is the highest score and 0.0 is the lowest. It applied 8 networks, each of which considers different features of the input decoys. Thus, Dove outputs 8 probability values.   
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
### Notice: Receptor chain ID must be 'A', ligand chain ID must be 'B' (PDB format)    
### Output record:    
Output will be saved in the subdirectory of your models' directory.       
For mode 0,the output record will be kept as file_name[:-4]_jobid[id].txt.    
For mode 1,the output record will be kept as RECORD_jobid[id].txt
### Output format(Example):   
complex.244440.pdb,0.80237,0.79943,0.90355,0.78516,-1.00000,-1.00000,0.91417,0.75000,     
(Explanation: 1st column is the file name, 2nd-9th column denotes the probability of the decoy is correct (acceptable quality according to CAPRI). If the value is -1, it means the model is not evaluated using the corresponding features.)
    
## Example: 
***Example pdb:Web/Example/Correct.pdb***
***Here is an example output of a correct decoy:***   
![](https://github.com/kiharalab/Dove_Pred/blob/master/Web/img/Correct.png)      
As you see in this example typically a correct decoy has a high probability (>0.5) from more than four feature combinations and no very small probability (< 0.01).     
      
***Here is an example output of an incorrect decoy:***      
![](https://github.com/kiharalab/Dove_Pred/blob/master/Web/img/Incorrect.png)  
Typically an incorrect decoy has at least one very small probability (< 0.01). 
     
***Explanation of different input features***   
![](https://github.com/kiharalab/Dove_Pred/blob/master/Web/img/input_instruction.png) 

