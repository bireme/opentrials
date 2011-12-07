#!/usr/bin/env python

cods = set()
nomes = set()
for lin in open('munic.txt'):
    lin = lin.strip()
    if not lin or lin.startswith('#'): continue
    uf, cod, nome = lin.split('\t')
    cods.add(cod)
    nomes.add(nome)

print len(cods), 'codigos distintos'
print len(nomes), 'nomes distintos'
print len(cods) - len(nomes), 'nomes repetidos'