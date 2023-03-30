from functions import open_query, check_validity_query, find_ortholog_groups_and_proteins, \
    write_ortholog_groups, add_gene_annotation, write_ortholog_result
import open_files as files
import lib.argparse as argparse
import lib.os as os

# Input is read from command line
f_o_parser = argparse.ArgumentParser()
f_o_parser.add_argument("input", help="file name the query file")
f_o_parser.add_argument("-v", "--verbose", action="store_true", help="All the proteinID's and ortholog groups will be "
                                                                     "saved in separate files")
args = f_o_parser.parse_args()
query = os.path.normpath(args.input)
verbose = args.verbose

# extracting query
species_a, species_b = open_query(query)

# checking validity
tax_id_a, tax_id_b = check_validity_query(species_a, species_b, files.species_list)

# cleaning names
species_a = species_a.replace(" ", "_")
species_b = species_b.replace(" ", "_")

# finding common orthologs
common_gene_groups, a_genes, b_genes = find_ortholog_groups_and_proteins(tax_id_a, tax_id_b, files.members_list)

# writing lists of the ortholog groups for each species
if verbose:
    write_ortholog_groups(common_gene_groups, a_genes, b_genes, species_a, species_b)

# adding information to them
common_gene_groups = add_gene_annotation(common_gene_groups, files.annotation_list)

# writing results on a text document
write_ortholog_result(common_gene_groups, species_a, species_b, verbose)


