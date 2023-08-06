import argparse
import os
import logging

import time
import pickle
import numpy as np
from rdkit import Chem
from Bio import SeqIO
import pandas as pd
from tqdm import tqdm
from utils import convert_molecule_into_graph, graph_dataset
from model.model import GINEConv_pretrain, GINEConv_train, model_prediction

import torch
from torch import nn 
from torch_geometric.loader import DataLoader



# Configuration
MODEL_CHECKPOINT_PATH = '/home/jihun/python/BGCFinder_build/model/BGC_finder_checkpoint'
##TO-DO : proper model download link

parser = argparse.ArgumentParser(description='BGCfinder - Biosynthetic Gene Cluster finder with Graph Neural Network')
parser.add_argument('input_faa_filename', type=str, help='input protein sequence in fasta format') 
parser.add_argument('-o','--output_filename', type=str, default='output.tsv', help='output file name') 
parser.add_argument('-l','--log_filename',  type=str, default='output.log', help='lig file name') 
parser.add_argument('-s', '--score_threshold', type=float, default=0.8, help='the probability threshold for BGC detection') 
parser.add_argument('-g', '--merge_max_protein_gap', type=float, default=0, help='the maximum number of gap in a cluster') 
parser.add_argument('-m', '--min_num_protein_in_cluster', type=float, default=2, help='the minimum numter of protein in a cluster') 
parser.add_argument('-d', '--gpu_usage', type=bool, default=False, help='the usage of GPU') 

input_faa_filename = parser.parse_args().input_faa_filename
output_filename = parser.parse_args().output_filename
log_filename = parser.parse_args().log_filename
if parser.parse_args().gpu_usage:
    DEVICE = 'cuda'
else:
    DEVICE = 'cpu'


logging.basicConfig(filename=log_filename, level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
#file_handler = logging.FileHandler(log_filename) # To output a long on the file
#file_handler.setFormatter(formatter) #format


# To read a fasta file from Prodigals
seq_records = SeqIO.parse(input_faa_filename,"fasta")
seq_BGCs_proteinID = []
seq_BGCs_geneID = []
seq_BGCs_fasta = []
seq_BGCs_description = []
for seq_record in seq_records:
    seq_BGCs_proteinID.append(str(seq_record.id))
    seq_BGCs_geneID.append(''.join((seq_record.id).split('.', 1)[:-1]))
    seq_BGCs_description.append(seq_record.description)
    if (str(seq_record.seq)[-1] == '*') : 
        #print('remove asterisk')
        seq_BGCs_fasta.append(str(seq_record.seq)[:-1])
    else :
        seq_BGCs_fasta.append(str(seq_record.seq))
        
fasta_df = pd.DataFrame({"proteinID": seq_BGCs_proteinID, "geneID": seq_BGCs_geneID, "description": seq_BGCs_description, "fasta": seq_BGCs_fasta})
del seq_records, seq_BGCs_proteinID, seq_BGCs_fasta, seq_BGCs_description

# to convert into a graph
num_df = fasta_df.shape[0]
print('The number of protein coding genes in the input file: ', num_df)
start_time = time.time()
input_graph = [0] *  num_df
skip_pos = 0
location = 0 # to save element in a list one by one
for iteration in tqdm(range(num_df)):
    fasta = Chem.MolFromFASTA(fasta_df.iloc[iteration].fasta)
    if fasta:
        input_graph[location] = convert_molecule_into_graph(mol= fasta, 
                                                    name=fasta_df.iloc[iteration].proteinID)
        location += 1
    else: 
        skip_pos += 1

input_graph = input_graph[:location]
finish_time = time.time()
print(f'the number of graph in a input file : {len(input_graph)}')
logging.debug(f'the number of graph in a input file : {len(input_graph)}')

# to prepare the data loader
input_dataset = graph_dataset(input_graph)
print("the number of dataset : ",len(input_dataset))
logging.debug(f'the number of dataset : {len(input_dataset)}')

input_loader = DataLoader(input_dataset, batch_size=1, shuffle=False, drop_last=False)
logging.debug(f'data loader works')
# to load model and its checkpoint
device = torch.device(DEVICE)
model = GINEConv_train(pretrain_model=GINEConv_pretrain(num_hidden= 15, num_node_features=12, num_edge_features=4, n_layers=150).to(device),
 out_channels=2).to(device)
checkpoint = torch.load(MODEL_CHECKPOINT_PATH)
model.load_state_dict(checkpoint['model_state_dict'])
logging.debug(f'model load is done')
proteinID, y_probability, y_pred = model_prediction(model, input_loader, DEVICE) 
logging.debug(f'model prediction is done')

gbc_score = pd.DataFrame({"proteinID":proteinID, "probability":y_probability, "label":y_pred})
input_df = gbc_score.sort_index()
score_threshold =  parser.parse_args().score_threshold
merge_max_protein_gap =  parser.parse_args().merge_max_protein_gap
min_num_protein_in_cluster =  parser.parse_args().min_num_protein_in_cluster
clusters = []
active_proteins = []
gap_proteins = []

# Create a list of cluster features by merging consecutive proteins with score satisfying given threshold
# Neighboring clusters within given number of nucleotides/proteins are merged
for iteration in range(len(input_df)):
    # Inactive protein (low probability), add to gap
    if input_df["probability"].iloc[iteration] < score_threshold : 
        gap_proteins.append(iteration)
        if active_proteins :
            clusters.append(active_proteins)
            active_proteins = []
    # Active protein (high probability)
    else :
        # If no cluster is open, check if we should merge with the previous cluster by gap
        if not active_proteins and clusters:
            prev_cluster_proteins = clusters[-1]
            #prev_end = prev_cluster_proteins[-1].location.end
            if len(gap_proteins) <= merge_max_protein_gap :
                #or \protein.location.start - prev_end) <= merge_max_nucl_gap
                # Remove previous candidate and continue where it left off
                clusters = clusters[:-1]
                active_proteins = prev_cluster_proteins + gap_proteins

        # Add current protein to cluster
        active_proteins.append(iteration)
        gap_proteins = []
# Last protein was active, add list of active proteins as a cluster
if active_proteins:
    clusters.append(active_proteins)

clusters = list(filter(lambda cluster: len(cluster) >= min_num_protein_in_cluster, clusters))
print("the number of clusters: ", len(clusters))
logging.debug(f'the number of clusters : {len(clusters)}')

# to save output
output_df = pd.DataFrame()
for i in range(len(clusters)):
    add_df = input_df.iloc[clusters[i]].copy()
    add_df['cluster'] = i # add a column of cluster index
    output_df = pd.concat([output_df, add_df], axis=0) #by row
    
output_df.to_csv(output_filename, index=False, header=True, sep="\t")
