from functions import compare_results, write_comp_result, yes_or_no
import argparse
import os

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

# test = {}
if only_first:
    genes_only_selected_sp = compare_results(genes_1, genes_2, only_first)
    # Writing the file
    if yes_or_no('Would you like to save that?'):
        write_comp_result(genes_only_selected_sp, genes_1, genes_2, only_first)

elif both:
    genes_only_selected_sp = compare_results(genes_1, genes_2, only_first)
    # Writing the file
    if yes_or_no('Would you like to save that?'):
        write_comp_result(genes_only_selected_sp, genes_1, genes_2, only_first)

else:
    print('Choose one of the algorithms. Either \'-both\' or \'-only\'!')
