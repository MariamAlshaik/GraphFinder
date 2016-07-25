#%matplotlib inline
import os, sys
import subprocess as sp
from itertools import cycle
import networkx as nx
import re
import ntpath
import shutil
import fnmatch
#from eden.util import display
# -----------------------------------------------------------------------------

class GraphFinder(object):
    def __init__(self):
        self.seprator = '_'
        pass
    

    def _read_sto_file(self, file_path =None):
        
        '''read a Sto file separate the extract the interesting information from the file
            it takes the file path and returns the head which is the information type and it's sequence'''
        
        head_mark0 = '#'
        head_mark1 = '='
        head_mark2 = 'G'
        head_mark3 = 'C'
        head_list = []
        sequence_list = []  

        read_file = open(file_path ,'r') 
        for line in read_file: 
            lines = list(line)
                # the read line is the head of the sequence write it in head list
            if lines[0] == head_mark0 and lines[1] == head_mark1 and lines[2] == head_mark2 and lines[3] == head_mark3:
                line = line.strip('#=GC ')            
                line = line.strip('\n')
                line = line.split(' ')
                line = filter(None, line)

                head = line[0]
                head_list.append(head)
                sequence = line[1].split()
                sequence_list.append(sequence)
                zip_head_seqs = zip(head_list, sequence_list)

        return zip_head_seqs
    

    def _identify_information_type(self, file_name, head_seq_list):
        
        '''recognize the different types of information extracted from step1
            it takes the zipped info from the funtion '_readStoFile' and returns a dictionary 
            that identify every type of information'''

        secondery_structure_s = []
        conservation_s = []
        conservation_stringth_s = []
        entropy_0_s = []
        entropy_1_s = []
        entropy_2_s = []
        entropy_3_s = []
        coveriation_s = []

        for i, elemant in enumerate(head_seq_list):
            info_item = head_seq_list[i]

            if info_item[0] == 'SS_cons':
                secondery_structure_s.append(str(info_item[1]))

            if info_item[0] == 'cons':
                conservation_s.append(str(info_item[1]))

            if info_item[0] == 'conss':
                conservation_stringth_s.append(info_item[1])

            if info_item[0] == 'col_entropy_0':
                entropy_0_s.append(info_item[1])

            if info_item[0] == 'col_entropy_1':
                entropy_1_s.append(info_item[1])

            if info_item[0] == 'col_entropy_2':
                entropy_2_s.append(info_item[1])

            if info_item[0] == 'col_entropy_3':
                entropy_3_s.append(info_item[1])   

            if info_item[0] == 'cov_SS_cons':
                coveriation_s.append(info_item[1])

        file_dictionary = {"ID_file name": file_name, "conservation": conservation_s, "secondery_structure": secondery_structure_s,
                           "conservation_stringth": conservation_stringth_s, "entropy_3": entropy_3_s, "covariation": coveriation_s}
        return file_dictionary

    
    def _filter_info(self, info_type):
        sequence = info_type['conservation']
        structure = info_type['secondery_structure']
        conservation_stringth = info_type['conservation_stringth']
        covariation = info_type['covariation']
        entropy_3 = info_type['entropy_3']

        sequence = sequence[0].strip('[\']')
        #print ('seq', sequence)
        structure = structure[0].strip('[\']')
        #print ('stru', structure)
        conservation_stringth = str(conservation_stringth[0]).strip('[\']')
        covariation = str(covariation).strip('[\']')
        entropy_3 = str(entropy_3[0]).strip('[\']')

        zip_info_type = zip(sequence,conservation_stringth,covariation,entropy_3)
        return sequence, structure, conservation_stringth, covariation, entropy_3
    

    def _build_graph(self, head, sequence, structure, conservation_stringth, covariation, entropy_3):

        '''build a Networkx graph with all type of info (the most general graph)
            this graph identifies the basepair relation beside the next relation between the nodes
            transform the general graph to the wanted graph based on parameters passed by 
            the '_graphParametersList' function'''
        
        open_pran = "<" or "(" or "[" or "{"
        close_pran = ">" or ")" or "]" or "}"
        stack_o = []
        stack_pos_o =[]
        stack_c = []

        G = nx.Graph()
        G.graph['graph_title']= head
        print G.graph


        for i, k in enumerate(structure):
            G.add_node(i)
 
            G.node[i]['key'] = sequence[i] + self.seprator + covariation[i] + self.seprator + conservation_stringth[i] + self.seprator + entropy_3[i]
            G.node[i]['seq'] = sequence[i]
            G.node[i]['cov'] = covariation[i]
            G.node[i]['cor'] = conservation_stringth[i]
            G.node[i]['ent'] = entropy_3[i]

            G.add_node(i, label = G.node[i]['key'])

            # connect with the next node 
            if i > 0:
                G.add_edge(i-1, i, label= 'x')

            #find basepair and connect them
            if structure[i] == open_pran:
                j = i
                stack_o.append(structure[j])
                stack_pos_o.append(j)
                open_len = len(stack_o)

            if structure[i] == close_pran:
                stack_c.append(structure[i])
                stack_o.pop()
                j = stack_pos_o.pop()
                G.add_edge(i, j, label = 'b')
        return G 
    

    def transform(self, G, use_seq = True, use_cov = True, use_cor = True, use_ent = True):
        
        '''regenerating the graph with the disered info'''
        for i in G.nodes():
             if use_seq == True:
                G.node[i]['label'] = G.node[i]['seq']
               
             if use_cov == True:
                 G.node[i]['label'] = G.node[i]['cov']
            
             if use_cor == True:
                 G.node[i]['label'] = G.node[i]['cor']
                
             if use_ent == True:
                 G.node[i]['label'] = G.node[i]['ent']

        
             if use_seq == True and use_cov == True:
                 G.node[i]['label'] = G.node[i]['seq'] + self.seprator + G.node[i]['cov']
            
             if use_seq == True and use_cor == True:
                 G.node[i]['label'] = G.node[i]['seq'] + self.seprator + G.node[i]['cor']

             if use_seq == True and use_ent == True:
                 G.node[i]['label'] = G.node[i]['seq'] + self.seprator + G.node[i]['ent']
                
             if use_seq == True and use_cor == True and use_cov == True and use_ent == True:
                 G.node[i]['label'] = G.node[i]['seq'] + self.seprator + G.node[i]['cor'] + self.seprator + G.node[i]['cov'] + self.seprator + G.node[i]['ent']


             if use_cov == True and use_seq == True:
                 G.node[i]['label'] = G.node[i]['cov'] + self.seprator + G.node[i]['seq']

             if use_cov == True and use_cor == True:
                 G.node[i]['label'] = G.node[i]['cov'] + self.seprator + G.node[i]['cor']

             if use_cov == True and use_ent == True:
                 G.node[i]['label'] = G.node[i]['cov'] + self.seprator + G.node[i]['ent']
                
             if use_cov == True and use_cor == True and use_seq == True and use_ent == True:
                 G.node[i]['label'] = G.node[i]['cov'] + self.seprator + G.node[i]['cor'] + self.seprator + G.node[i]['seq'] + self.seprator + G.node[i]['ent']

                
                
        return G

    def graphs_transform(self, Graphs, use_seq = True, use_cov = True, use_cor = True, use_ent = True):
        
        '''regenerating the graph with the disered info'''

	for k, G in enumerate(Graphs):

            for i in G.nodes():
                if use_seq == True:
                    G.node[i]['label'] = G.node[i]['seq']
               
                if use_cov == True:
                    G.node[i]['label'] = G.node[i]['cov']
            
                if use_cor == True:
                    G.node[i]['label'] = G.node[i]['cor']
                
                if use_ent == True:
                    G.node[i]['label'] = G.node[i]['ent']
        
                if use_seq == True and use_cov == True:
                    G.node[i]['label'] = G.node[i]['seq'] + self.seprator + G.node[i]['cov']
            
                if use_seq == True and use_cor == True:
                    G.node[i]['label'] = G.node[i]['seq'] + self.seprator + G.node[i]['cor']

	        if use_seq == True and use_ent == True:
                    G.node[i]['label'] = G.node[i]['seq'] + self.seprator + G.node[i]['ent']
                
                if use_seq == True and use_cor == True and use_cov == True and use_ent == True:
                    G.node[i]['label'] = G.node[i]['seq'] + self.seprator + G.node[i]['cor'] + self.seprator + G.node[i]['cov'] + self.seprator + G.node[i]['ent']
                
        return G

    #def transform(Graphs):
    	#for graph in Graphs:
	     #transform_graphs = self._node_transform(graph, use_seq=True, use_cov = False)


    def file_to_graph(self, file_path=None):
        
        '''Read one file
           -------------
            read one STO file, extract the desired info, and then build the graph
            it takes the STO file path and returns it's graph'''
        
        head = ntpath.splitext(ntpath.basename(file_path))[0]
        zip_head_seqs = self._read_sto_file(file_path)
        #print zip_head_seqs
        info_type = self._identify_information_type(head, zip_head_seqs)
        sequence, structure, conservation_stringth, covariation, entropy_3 = self._filter_info(info_type)
        graph = self._build_graph(head, sequence, structure, conservation_stringth, covariation, entropy_3)
        #graph = self._remodel_graph(head, sequence, structure, conservation_stringth, covariation, entropy_3)
        return graph

    

    def convert(self, directory = None):
        '''Read a directory
            ----------------
            read a folder of STO files and then call '_File_to_graph' function
            it takes a directory path and returns list of their graphs'''
        
        #graph_list = []
        graphs = []
        for file_name in os.listdir(directory):
            file_complete_path = os.path.join(directory, file_name)
            graph = self.file_to_graph(file_complete_path)
            graphs.append(graph)
        return graphs
