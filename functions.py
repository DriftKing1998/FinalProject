
def write_result(common_gene_groups, query, verbose):
    common_proteins_a = set({})
    common_proteins_b = set({})
    q = query.split("\\")[-1].split(".",1)[0]
    groups = open(f'results/result_{q}.tsv', 'w')
    groups.write(f'#ortholog\tfunction\tspecies_a\tspecies_b\n')
    for gene_group, proteins in common_gene_groups.items():
        #print(gene_group, proteins)
        #exit()
        groups.write(f'{gene_group}\t{proteins[2]}\t{", ".join(proteins[0])}\t{", ".join(proteins[1])}\n')
        common_proteins_a.update(proteins[0])
        common_proteins_b.update(proteins[1])

    if verbose:
        protein_file = open(f'results/proteins/{q}.proteinIDs.txt', 'w')

        protein_file.write(f'>{query.split("/")[-1].split(".",1)[0].split("_")[0]} (species a)\n')
        for protein in common_proteins_a:
            protein_file.write(f'{protein}\n')

        protein_file.write(f'>{query.split("/")[-1].split(".",1)[0].split("_")[1]} (species b)\n')
        # genes_b = open(f'results/proteins/species_b_{query.split("/")[-1].split(".",1)[0]}.proteinIDs.txt', 'w')
        for protein in common_proteins_b:
            protein_file.write(f'{protein}\n')

        print(f'\nFile \'species_a_{q}.proteinIDs.txt\' has been created in the results/proteins folder.')
        print(f'File \'species_b_{q}.proteinIDs.txt\' has been created in the results/proteins folder.')

    print(f'File \'result_{q}.tsv\' has been created in the results folder.\n')
    return common_proteins_a, common_proteins_b


def find_common_gene_groups_and_proteins(tax_id_a, tax_id_b, members):
    common_gene_groups = {}
    only_a_gene_groups = {}
    only_b_gene_groups = {}

    for gene_group in members:
        a_found = False
        b_found = False
        proteins_a = set({})
        proteins_b = set({})
        all_ids = gene_group[5].split(',')

        for current_id in all_ids:
            taxon_ID, protein_ID = current_id.split('.', 1)
            if int(taxon_ID) == tax_id_a:
                a_found = True
                proteins_a.add(protein_ID)
            if int(taxon_ID) == tax_id_b:
                b_found = True
                proteins_b.add(protein_ID)

        if a_found and b_found:
            common_gene_groups[str(gene_group[1]).rstrip()] = [proteins_a, proteins_b]
        elif a_found:
            only_a_gene_groups[str(gene_group[1]).rstrip()] = proteins_a
        elif b_found:
            only_b_gene_groups[str(gene_group[1]).rstrip()] = proteins_b

    return common_gene_groups, only_a_gene_groups, only_b_gene_groups


def open_query(query_path):
    query = open(query_path)
    counter = 0
    for sp in query:
        if counter == 0:
            species_a = sp.rstrip()
        else:
            species_b = sp.rstrip()
        counter += 1
    query.close()
    return species_a, species_b


def add_gene_annotation(common_gene_groups, annotations):
    print(f'{len(common_gene_groups)} annotations to add.')
    for key in common_gene_groups.keys():
        common_gene_groups[key] = common_gene_groups[key] + list(annotations.loc[annotations[1].isin([key])][5])
    return common_gene_groups


def write_ortholog_groups(file_dict_both, file_dict_a, file_dict_b, query):
    q = query.split("\\")[-1].split(".",1)[0]
    genes = open(f'results/orthologs/species_a_{q}.orthologs.txt', 'w')
    for gene in file_dict_a.keys():
        genes.write(gene+'\n')
    genes = open(f'results/orthologs/species_b_{q}.orthologs.txt', 'w')
    for gene in file_dict_b.keys():
        genes.write(gene+'\n')
    genes = open(f'results/orthologs/both_{q}.orthologs.txt', 'w')
    for gene in file_dict_both.keys():
        genes.write(gene+'\n')

    print(f'\nFile \'species_a_{q}.orthologs.txt\' has been created in the results/orthologs folder.')
    print(f'File \'species_b_{q}.orthologs.txt\' has been created in the results/orthologs folder.')
    print(f'File \'both_{q}.genesIDs.txt\' has been created in the results/orthologs folder.\n')


