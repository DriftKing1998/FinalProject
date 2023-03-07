
def write_result(ortholog_genes, query):
    common_proteins = set({})

    groups = open(f'results/result_{query.split("/")[-1].split(".",1)[0]}.tsv', 'w')
    for gene_group, proteins in ortholog_genes.items():
        groups.write(f'{gene_group}\t{", ".join(proteins[0])}\t{", ".join(proteins[1])}\n')
        common_proteins.update(proteins[0])

    genes = open(f'results/{query.split("/")[-1].split(".",1)[0]}.genes.txt', 'w')
    for protein in common_proteins:
        genes.write(f'{protein}\n')

    return common_proteins


def find_common_gene_groups(tax_id_a, tax_id_b, members):
    common_genes = {}

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
            common_genes[gene_group[1]] = [proteins_a, proteins_b]

    return common_genes


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
