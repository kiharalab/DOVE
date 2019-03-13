def Write_List(file_path,use_list):
    with open(file_path,'w') as file:
        for item in use_list:
            file.write(str(item)+',')