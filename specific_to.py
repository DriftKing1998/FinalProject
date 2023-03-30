from functions import open_query, check_validity_query, find_specific_to, add_gene_annotation, yes_or_no, write_spec_result
import open_files as files
import argparse
import os

# Input is read from command line
s_t_parser = argparse.ArgumentParser()
s_t_parser.add_argument("input", help="file path to the query file")
args = s_t_parser.parse_args()
query = os.path.normpath(args.input)

# extracting query
species_a, species_b = open_query(query)
tax_id_a, tax_id_b = check_validity_query(species_a, species_b, files.species_list)

# cleaning names
species_a = species_a.replace(' ', '_')
species_b = species_b.replace(' ', '_')

# finding genes only present in these taxa
specific_groups = find_specific_to(tax_id_a, tax_id_b, files.members_list)

# adding information to them
specific_groups = add_gene_annotation(specific_groups, files.annotation_list)

if yes_or_no('Do you want to save that?'):
    # writing the results
    write_spec_result(specific_groups, species_a, species_b)
