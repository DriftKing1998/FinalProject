import os
import glob

### CREATING RESULTS
answer = input('Do you want to add queries to the query folder? (y/n)').lower()
if answer == 'y':
    N = int(input('How many different queries do you want to copy into the query folder? '))
    queries = []
    for x in range(N):
        loc_query = os.path.normpath(input(f'Enter absolute file path to the query no#{x + 1}. '))
        assert loc_query, 'No, file found.'
        print(loc_query)
        os.system(f'copy {loc_query} tmp\\queries\\')

# get every query in the query folder
queries = glob.glob('tmp/queries/*')
# check if all files should be saved
verbose = False
verb = input('Save every file? (y/n) ').lower()
if verb == 'y':
    verbose = True
# go through every query in the query folder
for query in queries:
    print(os.path.normpath(query))
    os.system(f'python find_orthologs.py {query} {"-v" if verbose else ""}')
    os.system(f'move {query} tmp\\old_queries\\')

### COMPARING RESULTS
# Listing all calculated results for choosing
current_files = glob.glob("results/*.tsv")
print('\nAll results:')
for idx, file in enumerate(current_files):
    print(f'{idx} : {file}')

# Chose two results to compare
file_no = [int(input('\nWhich result do you want to compare? (type the index of first file) ')),
           int(input('\nWhich result do you want to compare? (type the index of second file) '))]

algo = input('Do you want the number of common orthologs? (type: \'b\')\tOr the number of orthologs only in the first '
             'group? (type : \'o\') ')

if algo == 'b':
    os.system(f'python compare_results.py {current_files[file_no[0]]} {current_files[file_no[1]]} -b')
elif algo == 'o':
    os.system(f'python compare_results.py {current_files[file_no[0]]} {current_files[file_no[1]]} -o')
