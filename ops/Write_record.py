import os
def Write_record(record,dir_path,pdb_id,random_id):
    record_path=os.path.join(dir_path,pdb_id+'_jobid'+str(int(random_id))+'.txt')
    with open(record_path,'w') as file:
        for tmp_record in record:
            for count,item in enumerate(tmp_record):
                if count==0:
                    file.write(item+',')#write file name
                    continue
                file.write('%.4f,'%item)
            file.write('\n')


