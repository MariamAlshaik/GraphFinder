import os, sys
import ntpath
import shutil
import fnmatch
#--------------------------------------

def classesToFolders(files_abs_path, partition_abs_path, pos_class_0_abs_path, pos_class_1_abs_path, neg_class_0_abs_path, neg_class_1_abs_path):

    '''seperate classes into diffeerent folders'''

    pos_partition_file = "positive-partitions-test.tab"
    neg_partition_file = "negative-partitions-test.tab"

    tab_list = os.listdir(partition_abs_path)
    for tab_file in os.listdir(partition_abs_path):
        files_list = os.listdir(files_abs_path)
        
        for folder_name in os.listdir(files_abs_path):
            folder_path = os.path.join(files_abs_path, folder_name)
            
            if tab_file == pos_partition_file and folder_name == 'positives-sto':
                read_pos_tab = open(os.path.join(partition_abs_path, tab_file), 'r')

                for line in read_pos_tab:
                    line_parts= line.split()
                    file_name = line_parts[0]
                    file_class_num = line_parts[1]

                    '''copy file to the pos_class_0 folder'''
                    if file_class_num == '0':
                        for file in os.listdir(folder_path):
                            file_path = os.path.join(folder_path, file)
                            file = ntpath.splitext( ntpath.basename(file_path))[0]
                            if fnmatch.fnmatch(file, file_name):
                                shutil.copy(file_path, pos_class_0_abs_path)
                            
                    '''copy file to the pos_class_1 folder'''
                    if file_class_num == '1':                      
                        for file in os.listdir(folder_path):
                            file_path = os.path.join(folder_path, file)
                            file = ntpath.splitext( ntpath.basename(file_path))[0]
                            if fnmatch.fnmatch(file, file_name):
                                shutil.copy(file_path, pos_class_1_abs_path)
                                
            if tab_file == neg_partition_file and folder_name == 'negatives-sto':
                read_neg_tab = open(os.path.join(partition_abs_path, tab_file), 'r')
                for line in read_neg_tab:
                    line_parts= line.split()
                    file_name = line_parts[0]
                    file_class_num = line_parts[1]
                    '''copy file to the pos_class_0 folder'''
                    if file_class_num == '0':
                        for file in os.listdir(folder_path):
                            file_path = os.path.join(folder_path, file)
                            file = ntpath.splitext( ntpath.basename(file_path))[0]
                            if fnmatch.fnmatch(file, file_name):
                                shutil.copy(file_path, neg_class_0_abs_path)

                    '''copy file to the pos_class_1 folder'''
                    if file_class_num == '1':
                        for file in os.listdir(folder_path):
                            file_path = os.path.join(folder_path, file)
                            file = ntpath.splitext( ntpath.basename(file_path))[0]
                            if fnmatch.fnmatch(file, file_name):
                                shutil.copy(file_path, neg_class_1_abs_path)
