import lib.pandas as pd
import lib.csv as csv

species_list = pd.read_table("data/species_list.tsv")
members_list = csv.reader(open("data/meNOG.members.tsv"), delimiter="\t")
annotation_list = pd.read_table("data/meNOG.annotations.tsv", header=None)
