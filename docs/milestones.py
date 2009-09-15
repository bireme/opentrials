#!/usr/bin/env python
# coding: utf-8

MILES = 'v0.6 v0.7 v0.8 v0.9 v1.0'.split()

def valor(s):
    try:
        return int(s)
    except ValueError:
        return 0

for off_mil, milestone in enumerate(MILES[:1]):
    print '== %s ==' % milestone

    miolo = False
    arq = open('milestones.txt')
    for lin in arq:
        lin = lin.rstrip()
        if not lin: continue
        lin = lin.decode('cp1252')
        partes = lin.split('\t')
        if partes[0] == '1':
            miolo = True
        if not miolo: continue 
        miles = []
        # x.y.z |descr| v0.6 | v0.7 | v0.8 | v0.9 | v1.0 | v2.0 |
        num, descr = partes[:2]
        miles[:] = (valor(s) for s in partes[2:2+len(MILES)])
        if len(num) < 5: 
            print '     %-5s %-40s ' % (num, descr,)
        if len(miles) > off_mil and miles[off_mil]:
            total = sum(miles)
            feito = sum(miles[:off_mil+1])/float(total)
            print '%3.f%% %-5s %-40s ' % (feito*100, num, descr,)

    arq.close()
