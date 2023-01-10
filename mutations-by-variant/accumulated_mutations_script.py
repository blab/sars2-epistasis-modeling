import json
from augur.utils import json_to_tree
import pandas as pd

# starting node
END_NODE = "NODE_0000260"

#grab lineage of tip node
def find_lineage(tree, child_node, rows_for_tsv):
    gene_muts = {}
    node_path = tree.get_path(child_node)
    i = len(node_path) - 1
    while (i >= 0 and node_path[i].name != END_NODE):
        i = i - 1
        gene_muts = format_string(node_path[i].branch_attrs['mutations'],'nuc', gene_muts)
    #append variant name, mutation, and region to list
    for k in gene_muts.keys():
        for j in range(len(gene_muts[k])):
            temp_dict = gene_muts[k]
            rows_for_tsv.append({'variant': child_node.name, 'mutation': str(temp_dict[j]), 'region': str(k)})

#put all the same gene mutations in the same list
def format_string(dict, key, gene_muts):
    for k in dict.keys():
        if (str(k) != key):
            if k not in gene_muts.keys():
                gene_muts[k] = []
            for j in range(len(dict[k])):
                temp_dict = dict[k]
                gene_muts[k].append(temp_dict[j])
    return gene_muts

if __name__ == '__main__':
    #read in tree
    with open(f'pango_lineages.json', 'r') as f:
        tree_json = json.load(f)
    #put tree in Bio.Phylo format
    tree = json_to_tree(tree_json)
    #create list of dictionaries for dataframe
    rows_for_tsv = []
    for tip in tree.find_clades(terminal=True):
        #append new row for every mutation in every child node
        find_lineage(tree, tip, rows_for_tsv)
    #make pandas dataframe from list of dicts
    df = pd.DataFrame(rows_for_tsv)
    #save dataframe as tsv
    df.to_csv('accumulated_mutations_output.tsv', sep='\t')
