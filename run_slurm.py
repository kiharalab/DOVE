import argparse
import os
from ops.os_operation import mkdir
#I have add "module load slurm" in .bashrc
#I have add "module load cuda/9.0" in .bashrc
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-F', type=str, required=True, help='decoy example path')  # File path for our MAINMAST code
    parser.add_argument('--id', type=int, default=888,
                        help='random id for the webserver notification, make sure corresponding')
        # Dense points part parameters
    args = parser.parse_args()
    params = vars(args)
    command_line = '/usr/bin/python3 main.py --mode=0  -F ' + str(params['F'])+' --id='+str(params['id'])+' --gpu=5'
    #In default,we do not use gpu.
    log_path = os.path.join(os.getcwd(), 'log')
    file_path=os.path.abspath(params['F'])
    mkdir(log_path)
    split_lists=os.path.split(file_path)
    tmp_log_path = os.path.join(log_path, split_lists[1]+ '_jobid' + str(params['id']) + '.txt')
    batch_file = os.path.join(log_path, 'slurm-job' + str(split_lists[1]) + '.sh')
    with open(batch_file, 'w') as file:
        file.write('#!/usr/bin/env bash\n')
        file.write('\n')
        file.write('#SBATCH -o ' + tmp_log_path + '\n')
        file.write('#SBATCH -p kihara-gpu\n')
        file.write('#SBATCH --cpus-per-task=1\n')
        file.write('#SBATCH --ntasks=1\n')
        file.write(command_line + '\n')
    os.system('sbatch ' + batch_file)