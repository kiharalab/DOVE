import os
def Correct_WrongFormat(pdb_file):
    new_path=pdb_file[:-4]+'tmp'+pdb_file[-4:]
    with open(new_path,'w') as wfile:

        with open(pdb_file,'r') as rfile:
            line=rfile.readline()
            while line:
                name = line[(13 - 1):(16 - 1 + 1)]
                sname = name.strip()
                if len(sname) == 1:
                    q = " %s  " % sname
                elif len(sname) == 2:
                    q = " %s " % sname
                elif len(sname) == 3:
                    q = " %s" % sname
                elif len(sname) == 4:
                    q = sname
                else:
                    print(line)
                    print("[error] encountered blank atom name")
                    line = rfile.readline()
                    continue
                newname = line[:13 - 1] + q + line[16:]
                newname = newname
                wfile.write(newname)

                line=rfile.readline()
    os.system('mv '+new_path+' '+pdb_file)