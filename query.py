# query = open('tmp/chimp.txt')
query = open('tmp/mouse.txt')


counter = 0
for sp in query:
    if counter == 0:
        species_a = sp.rstrip()
    else:
        species_b = sp.rstrip()
    counter += 1


# Chimp : 13511
# Mouse : 12565

