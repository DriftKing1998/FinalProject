import pandas as pd
import sys
import argparse

# Input is read from command line
parser = argparse.ArgumentParser()
parser.add_argument("input1", help="file name of first tsv-file")
parser.add_argument("input2", help="file name of second tsv-file")
parser.add_argument("-b", "--both", action="store_true", help="Finds common gene-groups for both tsv-files")
parser.add_argument("-o", "--only", action="store_true", help="Finds gene-groups which are only in the first tsv-file")
args = parser.parse_args()
genes_1 = args.input1
genes_2 = args.input2
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
# chimp_result = pd.read_table(f'results/{genes_1.split("/")[1].split("_")[0]}_{genes_1.split("/")[1].split("_")[0]}_results.tsv')


# test = {}
if only_first:
    c_a = 0
    c_b = 0
    print('Filtering gene groups only in first file..')
    for gene_c in list(genes_1_data['#ortholog'].values):
        if gene_c not in list(genes_2_data['#ortholog'].values):
            genes_only_selected_sp.append(gene_c)
            c_a += len(list(genes_1_data.loc[genes_1_data['#ortholog'] == gene_c]['species_a'])[0].split(', '))
            c_b += len(list(genes_1_data.loc[genes_1_data['#ortholog'] == gene_c]['species_b'])[0].split(', '))

    print(f'\nOrtholog groups only in FIRST FILE: {len(genes_only_selected_sp)}\n'
          f'These correspond to {c_a} different genes for species a of the first file.\n'
          f'These correspond to {c_b} different genes for species b of the first file.')
elif both:
    c_a1 = 0
    c_a2 = 0
    c_b1 = 0
    c_b2 = 0
    print('Filtering common gene groups...')
    for gene_c in list(genes_1_data['#ortholog'].values):
        if gene_c in list(genes_2_data['#ortholog'].values):
            genes_only_selected_sp.append(gene_c)
            c_a1 += len(list(genes_1_data.loc[genes_1_data['#ortholog'] == gene_c]['species_a'])[0].split(', '))
            c_b1 += len(list(genes_1_data.loc[genes_1_data['#ortholog'] == gene_c]['species_b'])[0].split(', '))
            c_a2 += len(list(genes_2_data.loc[genes_2_data['#ortholog'] == gene_c]['species_a'])[0].split(', '))
            c_b2 += len(list(genes_2_data.loc[genes_2_data['#ortholog'] == gene_c]['species_b'])[0].split(', '))

    g1 = genes_1.split('\\')[1]
    g2 = genes_2.split('\\')[1]
    print(f'\nOrtholog groups in BOTH FILES: {len(genes_only_selected_sp)}\n'
          f'These correspond to {c_a1} different genes for species a of {g1}.\n'
          f'These correspond to {c_b1} different genes for species b of {g1}.\n'
          f'These correspond to {c_a2} different genes for species a of {g2}.\n'
          f'These correspond to {c_b2} different genes for species b of {g2}.')
else:
    print('Choose one of the algorithms. Either \'-both\' or \'-only\'!')
