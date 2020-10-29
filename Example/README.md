# Examples for Input and Output
Here We include a simple example of our model's input and output during the evaluation process.  
(1) We include the input pdb files in "Decoys" directory. All the inputs follow the pdb format. Also, to help our model recognize the receptor and ligand parts in the decoy, please keep in mind that Receptor chain ID must be 'A', ligand chain ID must be 'B'.   
(2) To generate features for goap and atom parts, our code will automatically generate the goap and itscore input. To help you better understand it's format, we keep the generated *_goap.pdb and *_itscore.pdb in "Generated_Input" directory.   
(3) Based on the pdb files and generated goap and itscore files, we generated the input for out model. We keep those input numpy files in the "Generated_Input" directory with the feature names.
(4) Finally, we keep the output probability file in the "Output" directory. (Explanation: 1st column is the file name, 2nd-9th column denotes the probability of the decoy is correct (acceptable quality according to CAPRI). If the value is -1, it means the model is not evaluated using the corresponding features.)   
Notes: Here we have -1 output for all ITScore related features because of we are not allowed to redistribute ITScore in our codes.

# Training Examples
To help you train your own model based on your own feature, we include training examples in "Training_Example" directory.  
(1) The training input should be pdb files and the label should be txt files, which is kept in "Training_Example" directory. They will automatically match with each other by indexes in their name.
(2) If you only use pdb files to build model like we did for ATOM40 features, the example input pdb files are included in "decoys" subdirectory of "Training_Example" directory.      
(3) If you have your own validation dataset, please specify the directory path with "-F1" command parameters. Otherwise, we will default randomly split 20% percent data as validation data.   
(4) If you want to add more features, we have included goap input example files in "Goap_Example_File" subdirectory of "Training_Example" directory and itscore input example files in "ITScore_Example_File" subdirectory of "Training_Example" directory.    
(5) To help you add more features and training, I added very detailed comments in [Training](https://github.com/kiharalab/DOVE/tree/master/Training) directory of this repo.   

Any questions, feel free to make contact with us: dkihara@purdue.edu

