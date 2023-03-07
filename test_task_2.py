genes_only_in_chimp = set({})

chimp = []
mouse = []

for c_line in open('results/chimp.genes.txt'):
    chimp.append(c_line.rstrip())

for m_line in open('results/mouse.genes.txt'):
    mouse.append(m_line.rstrip())

for gene in chimp:
    if gene not in mouse:
        genes_only_in_chimp.add(gene)

print(len(genes_only_in_chimp))



