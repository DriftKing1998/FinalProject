import pandas as pd

genes_1 = 'results/orthologs/both_human_chimp.orthologs.txt'
genes_2 = 'results/orthologs/species_a_human_mouse.orthologs.txt'


genes_1_data = pd.read_table(genes_1, header=None)
genes_2_data = pd.read_table(genes_2, header=None)

res = []
counter = 0
gen_2 = list(genes_2_data[0])
for x in genes_1_data[0]:
    if x in gen_2:
        counter += 1
        res.append(x)

print(counter)
print(res)

dict_ortholog_chimp = 'results/result_human_chimp.tsv'
dict_ortholog_chimp_data = pd.read_table(dict_ortholog_chimp)

counter_2 = 0
for x in res:
    tmp = list(dict_ortholog_chimp_data.loc[dict_ortholog_chimp_data['#ortholog'] == x]['species_a'])[0]
    print(tmp)
    print(len(tmp.split(', ')))
    counter_2 += len(tmp.split(', '))
print(counter_2)
