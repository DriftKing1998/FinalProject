import lib.os as os
import lib.glob as glob
from functions import yes_or_no


def f_o_script():
    # check if all files should be saved
    verbose = False
    if yes_or_no('Do you want to save every intermediate result file (every ortholog group & gene as text-file '
                 'files)?'):
        verbose = True
    # show queries
    current_queries = glob.glob("all_queries\\queries\\*.txt")
    print('\nAll queries:')
    for idx, file in enumerate(current_queries):
        print(f'{idx} : {file}')
    # ask which queries
    if yes_or_no('Do you want to run the algorithm on all queries?'):
        # go through every query in the query folder
        for query in current_queries:
            print(os.path.normpath(query))
            os.system(f'python find_orthologs.py {query} {"-v" if verbose else ""}')
            os.system(f'move {query} all_queries\\old_queries\\')
    else:
        # Chose query
        file_no = int(input('\nWhich query do you want to use? (type index of the file) '))
        assert file_no in range(len(current_queries)), 'There is no file with this index.'
        print(os.path.normpath(current_queries[file_no]))
        os.system(f'python find_orthologs.py {current_queries[file_no]} {"-v" if verbose else ""}')
        os.system(f'move {current_queries[file_no]} all_queries\\old_queries\\')


def c_r_script():
    # Listing all calculated results for choosing
    current_files = glob.glob("results/result_*.tsv")
    print('\nAll results:')
    for idx, file in enumerate(current_files):
        print(f'{idx} : {file}')

    # Chose two results to compare
    file_no = [int(input('\nWhich result do you want to compare? (type the index of first file) ')),
               int(input('Which result do you want to compare? (type the index of second file) '))]
    assert set(file_no).issubset(range(len(current_files))), 'There is no file with this index.'

    # Chose the algorithm with which to compare
    algo = input('Do you want the number of common orthologs (type: \'b\'), or the number of orthologs only in the '
                 'first group? (type : \'o\') ')
    if algo == 'b':
        os.system(f'python compare_results.py {current_files[file_no[0]]} {current_files[file_no[1]]} -b')
    elif algo == 'o':
        os.system(f'python compare_results.py {current_files[file_no[0]]} {current_files[file_no[1]]} -o')


def s_t_script():
    # Listing all possible queries
    current_queries = glob.glob("all_queries\\queries\\*.txt")
    print('\nAll queries:')
    for idx, file in enumerate(current_queries):
        print(f'{idx} : {file}')
    if yes_or_no('Do you want to run the algorithm on all queries?'):
        for query in current_queries:
            print(os.path.normpath(query))
            os.system(f'python specific_to.py {query}')
            os.system(f'move {query} all_queries\\old_queries\\')
    else:
        # Chose query
        file_no = int(input('\nWhich query do you want to use? (type index of the file) '))
        assert file_no in range(len(current_queries)), 'There is no file with this index.'
        print(os.path.normpath(current_queries[file_no]))
        os.system(f'python specific_to.py {current_queries[file_no]}')
        os.system(f'move {current_queries[file_no]} all_queries\\old_queries\\')
