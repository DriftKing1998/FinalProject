from scripts import *

if yes_or_no('Do you want to add queries to the query folder?'):
    loc_query = os.path.normpath(input(f'Enter absolute file path to the queries. '))
    assert loc_query, 'No, file found.'
    os.system(f'copy {loc_query} tmp\\queries\\')

# CREATING RESULTS
if yes_or_no('\nDo you want to use the \'find_orthologs\' function?'):
    f_o_script()

# COMPARING RESULTS
if yes_or_no('\nDo you want to use the \'compare_results\' function?'):
    c_r_script()

# CREATING RESULTS
if yes_or_no('\nDo you want to use the \'specific_to\' function?'):
    s_t_script()
