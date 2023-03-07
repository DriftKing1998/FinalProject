import sys
from functions import *
import open_files as files

# extracting query
query = sys.argv[1]
species_a, species_b = open_query(query)


# checking validity for species_a
assert species_a in files.species_list['#species name'].values, f'The species \'{species_a}\' is not listed in ' \
                                                                   f'the database '
tax_id_a = files.species_list.loc[files.species_list['#species name'] == species_a]['tax id'].values[0]
print(files.species_list.loc[files.species_list['#species name'] == species_a])

# checking validity for species_b
assert species_b in files.species_list['#species name'].values, f'The species \'{species_b}\' is not listed in ' \
                                                                   f'the database '
tax_id_b = files.species_list.loc[files.species_list['#species name'] == species_b]['tax id'].values[0]
print(files.species_list.loc[files.species_list['#species name'] == species_b])


# finding common genes
common_gene_groups = find_common_gene_groups(tax_id_a, tax_id_b, files.members_list)

# print(len(common_gene_groups))
# print(20345 - 19017)

# writing results on a text document
common_genes = write_result(common_gene_groups, query)


