import pandas as pd
import csv

species_list = pd.read_table("data/species_list.tsv")
members_list = csv.reader(open("data/meNOG.members.tsv"), delimiter="\t")
annotation_list = pd.read_table("data/meNOG.annotations.tsv", header=None)

#first = species_list.loc[species_list['#species name'] == 'Sinorhizobium fredii NGR234']
#print(species_list.loc[species_list['#species name'] == 'Homo sapiens'])
#print(first['core/periphery/adherent'])
