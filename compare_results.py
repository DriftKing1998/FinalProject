import pandas as pd
import os
import argparse
from functions import *

# Input is read from command line
parser = argparse.ArgumentParser()
parser.add_argument("input1", help="file name of first tsv-file")
parser.add_argument("input2", help="file name of second tsv-file")
parser.add_argument("-b", "--both", action="store_true", help="Finds common gene-groups for both tsv-files")
parser.add_argument("-o", "--only", action="store_true", help="Finds gene-groups which are only in the first tsv-file")
args = parser.parse_args()
genes_1 = os.path.normpath(args.input1)
genes_2 = os.path.normpath(args.input2)
both = args.both
only_first = args.only
assert not (both and only_first), f'Cannot perform both algorithms at the same time!'

# extracting query
# genes_1 = 'results/result_human_chimp.tsv'
# genes_2 = 'results/result_human_mouse.tsv'

genes_only_selected_sp = []
proteins_only_selected_sp = []

genes_1_data = pd.read_table(genes_1)
genes_2_data = pd.read_table(genes_2)
g1_sp1, g1_sp2 = [x.replace(" ", "_") for x in genes_1_data.columns.tolist()[-2:]]
g2_sp1, g2_sp2 = [x.replace(" ", "_") for x in genes_2_data.columns.tolist()[-2:]]

# test = {}
if only_first:
    c_a = 0
    c_b = 0
    print('Filtering gene groups only in first file..')
    for gene_c in list(genes_1_data['ortholog'].values):
        if gene_c not in list(genes_2_data['ortholog'].values):
            genes_only_selected_sp.append(gene_c)
            c_a += len(list(genes_1_data.loc[genes_1_data['ortholog'] == gene_c][g1_sp1])[0].split(', '))
            c_b += len(list(genes_1_data.loc[genes_1_data['ortholog'] == gene_c][g1_sp2])[0].split(', '))
    g1 = genes_1.split('\\')[1]
    g2 = genes_2.split('\\')[1]
    print(f'\nOrtholog groups only in FIRST FILE: {len(genes_only_selected_sp)}\n'
          f'These correspond to {c_a} different genes for {g1_sp1}.\n'
          f'These correspond to {c_b} different genes for {g1_sp2}.')

    # Writing the file
    if yes_or_no('Would you like to save that?'):
        write_comp_result(genes_only_selected_sp, genes_1, genes_2, only_first)
        '''only_groups = open(f'results/only_{g1.split(".")[0]}.tsv', 'w')
        only_groups.write(f'ortholog\tfunction\t{g1_sp1}\t{g1_sp2}\n')
        for gene in genes_only_selected_sp:
            tmp = "\t".join(list(genes_1_data.loc[genes_1_data["ortholog"] == gene].values[0]))
            only_groups.write(f'{tmp}\n')
        print(f'\nThese proteins/ortholog-groups have been saved in the results folder: \'only_{g1.split(".")[0]}.tsv\'')'''

elif both:
    c_a1 = 0
    c_a2 = 0
    c_b1 = 0
    c_b2 = 0
    print('Filtering common gene groups...')
    for gene_c in list(genes_1_data['ortholog'].values):
        if gene_c in list(genes_2_data['ortholog'].values):
            genes_only_selected_sp.append(gene_c)
            c_a1 += len(list(genes_1_data.loc[genes_1_data['ortholog'] == gene_c][g1_sp1])[0].split(', '))
            c_b1 += len(list(genes_1_data.loc[genes_1_data['ortholog'] == gene_c][g1_sp2])[0].split(', '))
            c_a2 += len(list(genes_2_data.loc[genes_2_data['ortholog'] == gene_c][g2_sp1])[0].split(', '))
            c_b2 += len(list(genes_2_data.loc[genes_2_data['ortholog'] == gene_c][g2_sp2])[0].split(', '))

    g1 = genes_1.split('\\')[1]
    g2 = genes_2.split('\\')[1]
    print(f'\nOrtholog groups in BOTH FILES: {len(genes_only_selected_sp)}\n'
          f'These correspond to {c_a1} different genes for {g1_sp1}.\n'
          f'These correspond to {c_b1} different genes for {g1_sp2}.\n'
          f'These correspond to {c_a2} different genes for {g2_sp1}.\n'
          f'These correspond to {c_b2} different genes for {g2_sp2}.')

    # Writing the file
    if yes_or_no('Would you like to save that?'):
        write_comp_result(genes_only_selected_sp, genes_1, genes_2, only_first)
        '''n1 = g1.split(".")[0].split("_", 1)[1]
        n2 = g2.split(".")[0].split("_", 1)[1]
        common_groups = open(f'results/common_{n1}_{n2}.tsv', 'w')
        common_groups.write(f'ortholog\tfunction\t{g1_sp1}\t{g1_sp2}\t{g2_sp1}\t{g2_sp2}\n')
        for gene in genes_only_selected_sp:
            tmp1 = "\t".join(list(genes_1_data.loc[genes_1_data["ortholog"] == gene].values[0]))
            tmp2 = "\t".join(list(genes_2_data.loc[genes_2_data["ortholog"] == gene].values[0])[2:])
            common_groups.write(f'{tmp1}\t{tmp2}\n')
        print(
            f'\nThese proteins/ortholog-groups have been saved in the results folder: \'only_{g1.split(".")[0]}.tsv\'')'''

else:
    print('Choose one of the algorithms. Either \'-both\' or \'-only\'!')
