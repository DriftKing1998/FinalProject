import lib.pandas as pd


def check_validity_query(species_a, species_b, species_list):
    # checking validity for species_a
    assert species_a in species_list['#species name'].values, f'The species \'{species_a}\' is not listed in ' \
                                                                    f'the database '
    tax_id_a = species_list.loc[species_list['#species name'] == species_a]['tax id'].values[0]
    print(species_list.loc[species_list['#species name'] == species_a])

    # checking validity for species_b
    assert species_b in species_list['#species name'].values, f'The species \'{species_b}\' is not listed in ' \
                                                                    f'the database '
    tax_id_b = species_list.loc[species_list['#species name'] == species_b]['tax id'].values[0]
    print(species_list.loc[species_list['#species name'] == species_b])
    return tax_id_a, tax_id_b


def write_ortholog_result(common_gene_groups, tax_id_a, tax_id_b, verbose):
    common_proteins_a = set({})
    common_proteins_b = set({})
    groups = open(f'results/result_{tax_id_a}_{tax_id_b}.tsv', 'w')
    groups.write(f'ortholog\tfunction\t{tax_id_a}\t{tax_id_b}\n')

    for gene_group, proteins in common_gene_groups.items():
        if type(proteins[2]) == float:
            groups.write(f'{gene_group}\tUnknown\t{", ".join(proteins[0])}\t{", ".join(proteins[1])}\n')
        else:
            groups.write(f'{gene_group}\t{proteins[2]}\t{", ".join(proteins[0])}\t{", ".join(proteins[1])}\n')
        common_proteins_a.update(proteins[0])
        common_proteins_b.update(proteins[1])

    if verbose:
        protein_file = open(f'results/proteins/{tax_id_a}_{tax_id_b}.proteinIDs.txt', 'w')

        protein_file.write(f'>{tax_id_a}\n')
        for protein in common_proteins_a:
            protein_file.write(f'{protein}\n')

        protein_file.write(f'>{tax_id_b}\n')
        # genes_b = open(f'results/proteins/species_b_{query.split("/")[-1].split(".",1)[0]}.proteinIDs.txt', 'w')
        for protein in common_proteins_b:
            protein_file.write(f'{protein}\n')

        print(f'\nFile \'{tax_id_a}.proteinIDs.txt\' has been created in the results/proteins folder.')
        print(f'File \'{tax_id_b}.proteinIDs.txt\' has been created in the results/proteins folder.')

    print(f'File \'result_{tax_id_a}_{tax_id_b}.tsv\' has been created in the results folder.\n')
    return True


def write_comp_result(genes_only_selected_sp, genes_1, genes_2, only_first):
    # Getting data needed
    genes_1_data = pd.read_table(genes_1)
    genes_2_data = pd.read_table(genes_2)
    g1_sp1, g1_sp2 = [x.replace(" ", "_") for x in genes_1_data.columns.tolist()[-2:]]
    g2_sp1, g2_sp2 = [x.replace(" ", "_") for x in genes_2_data.columns.tolist()[-2:]]
    g1 = genes_1.split('\\')[1].split(".")[0].split("_", 1)[1]
    g2 = genes_2.split('\\')[1].split(".")[0].split("_", 1)[1]

    # 'only first' or 'both'
    if only_first:
        only_groups = open(f'results/only_{g1}_not_{g2}.tsv', 'w')
        only_groups.write(f'ortholog\tfunction\t{g1_sp1}\t{g1_sp2}\n')
        for gene in genes_only_selected_sp:
            tmp = "\t".join(list(genes_1_data.loc[genes_1_data["ortholog"] == gene].values[0]))
            only_groups.write(f'{tmp}\n')
        print(f'\nThese proteins/ortholog-groups have been saved in the results folder: \'only_{g1}_not_{g2}.tsv\'')
    else:
        common_groups = open(f'results/common_{g1}_{g2}.tsv', 'w')
        common_groups.write(f'ortholog\tfunction\t{g1_sp1}\t{g1_sp2}\t{g2_sp1}\t{g2_sp2}\n')
        for gene in genes_only_selected_sp:
            tmp1 = "\t".join(list(genes_1_data.loc[genes_1_data["ortholog"] == gene].values[0]))
            tmp2 = "\t".join(list(genes_2_data.loc[genes_2_data["ortholog"] == gene].values[0])[2:])
            common_groups.write(f'{tmp1}\t{tmp2}\n')
        print(
            f'\nThese proteins/ortholog-groups have been saved in the results folder: \'common_{g1}_{g2}.tsv\'')

    return True


def write_spec_result(common_gene_groups, tax_id_a, tax_id_b):
    groups = open(f'results/specific_to_{tax_id_a}_{tax_id_b}.tsv', 'w')
    groups.write(f'ortholog\tfunction\t{tax_id_a}\t{tax_id_b}\n')

    for gene_group, proteins in common_gene_groups.items():
        if type(proteins[2]) == float:
            groups.write(f'{gene_group}\tUnknown\t{", ".join(proteins[0])}\t{", ".join(proteins[1])}\n')
        else:
            groups.write(f'{gene_group}\t{proteins[2]}\t{", ".join(proteins[0])}\t{", ".join(proteins[1])}\n')

    print(f'File \'specific_to_{tax_id_a}_{tax_id_b}.tsv\' has been created in the results folder.\n')
    return True


def write_ortholog_groups(file_dict_both, file_dict_a, file_dict_b, species_a, species_b):
    genes = open(f'results/orthologs/{species_a}_NOT_{species_b}.orthologs.txt', 'w')
    for gene in file_dict_a.keys():
        genes.write(gene + '\n')
    genes = open(f'results/orthologs/{species_b}_NOT_{species_a}.orthologs.txt', 'w')
    for gene in file_dict_b.keys():
        genes.write(gene + '\n')
    genes = open(f'results/orthologs/{species_a}_AND_{species_b}.orthologs.txt', 'w')
    for gene in file_dict_both.keys():
        genes.write(gene + '\n')

    print(f'\nFile \'{species_a}_NOT_{species_b}.orthologs.txt\' has been created in the results/orthologs folder.')
    print(f'File \'{species_b}_NOT_{species_a}.orthologs.txt\' has been created in the results/orthologs folder.')
    print(f'File \'{species_a}_AND_{species_b}.orthologs.txt\' has been created in the results/orthologs folder.')


def find_ortholog_groups_and_proteins(tax_id_a, tax_id_b, members):
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


def compare_results(genes_1, genes_2, only_first):
    genes_1_data = pd.read_table(genes_1)
    genes_2_data = pd.read_table(genes_2)
    g1_sp1, g1_sp2 = [x.replace(" ", "_") for x in genes_1_data.columns.tolist()[-2:]]
    g2_sp1, g2_sp2 = [x.replace(" ", "_") for x in genes_2_data.columns.tolist()[-2:]]
    genes_only_selected_sp = []
    c_a1 = 0
    c_a2 = 0
    c_b1 = 0
    c_b2 = 0
    if only_first:
        print('Filtering gene groups only in first file...')
        for gene_c in list(genes_1_data['ortholog'].values):
            if gene_c not in list(genes_2_data['ortholog'].values):
                genes_only_selected_sp.append(gene_c)
                c_a1 += len(list(genes_1_data.loc[genes_1_data['ortholog'] == gene_c][g1_sp1])[0].split(', '))
                c_b1 += len(list(genes_1_data.loc[genes_1_data['ortholog'] == gene_c][g1_sp2])[0].split(', '))

        print(f'\nOrtholog groups only in FIRST FILE: {len(genes_only_selected_sp)}\n'
              f'These correspond to {c_a1} different genes for {g1_sp1}.\n'
              f'These correspond to {c_b1} different genes for {g1_sp2}.')
    else:
        print('Filtering common gene groups...')
        for gene_c in list(genes_1_data['ortholog'].values):
            if gene_c in list(genes_2_data['ortholog'].values):
                genes_only_selected_sp.append(gene_c)
                c_a1 += len(list(genes_1_data.loc[genes_1_data['ortholog'] == gene_c][g1_sp1])[0].split(', '))
                c_b1 += len(list(genes_1_data.loc[genes_1_data['ortholog'] == gene_c][g1_sp2])[0].split(', '))
                c_a2 += len(list(genes_2_data.loc[genes_2_data['ortholog'] == gene_c][g2_sp1])[0].split(', '))
                c_b2 += len(list(genes_2_data.loc[genes_2_data['ortholog'] == gene_c][g2_sp2])[0].split(', '))

        print(f'\nOrtholog groups in BOTH FILES: {len(genes_only_selected_sp)}\n'
              f'These correspond to {c_a1} different genes for {g1_sp1}.\n'
              f'These correspond to {c_b1} different genes for {g1_sp2}.\n'
              f'These correspond to {c_a2} different genes for {g2_sp1}.\n'
              f'These correspond to {c_b2} different genes for {g2_sp2}.')
    return genes_only_selected_sp


def find_specific_to(ID_a, ID_b, members):
    both = 0
    only_a = 0
    only_b = 0
    IDs = [ID_a, ID_b]
    specific_genes = {}
    for gene_group in members:
        a_found = False
        b_found = False
        smt_else = False
        proteins_a = []
        proteins_b = []
        all_ids = gene_group[5].split(',')

        for current_id in all_ids:
            taxon_ID, protein_ID = current_id.split('.', 1)
            if int(taxon_ID) not in IDs:
                smt_else = True
                break
            if int(taxon_ID) == ID_a:
                a_found = True
                proteins_a.append(protein_ID)
            if int(taxon_ID) == ID_b:
                b_found = True
                proteins_b.append(protein_ID)

        if smt_else:
            continue
        elif a_found and b_found:
            specific_genes[str(gene_group[1]).rstrip()] = [proteins_a, proteins_b]
            both += 1
        elif a_found:
            specific_genes[str(gene_group[1]).rstrip()] = [proteins_a, []]
            only_a += 1
        elif b_found:
            specific_genes[str(gene_group[1]).rstrip()] = [[], proteins_b]
            only_b += 1

    print(f'\nThere are {sum([both, only_a, only_b])} ortholog groups specific to these taxa.\n'
          f'{both} are represented in both species.\n'
          f'{only_a} are represented only in {get_species_name(ID_a)}.\n'
          f'{only_b} are represented only in {get_species_name(ID_b)}.')

    return specific_genes


def yes_or_no(question):
    answer = input(f'{question} (y/n)').lower()
    if answer == 'y':
        return True
    elif answer == 'n':
        return False
    else:
        return yes_or_no(question)


def open_query(query_path):
    species_a, species_b = open(query_path)
    return species_a.strip(), species_b.strip()


def add_gene_annotation(common_gene_groups, annotations):
    print(f'\n{len(common_gene_groups)} annotations to add...\n')
    for key in common_gene_groups.keys():
        common_gene_groups[key] = common_gene_groups[key] + list(annotations.loc[annotations[1].isin([key])][5])
    return common_gene_groups


def get_taxID(sp, species):
    return int(species.loc[species['#species name'] == sp]['tax id'])


def get_species_name(ID):
    from open_files import species_list
    return str(species_list.loc[species_list['tax id'] == ID]['#species name'].values[0])
