#!/usr/bin/env python
# -*- coding: utf-8 -*-

OUTPUTSDIR='tcase/outputs/'

class SimMatrix:
    def __init__(self, simName):
        self.simName = simName
        self._m = {}
        self._N = 0

    def init_from_files(self, files):
        self._files = files
        self._N = len(files)
        for i in range(self._N):
            self._m[i] = {}
            for j in range(self._N):
                self._m[i][j] = 0

    def set(self, i, j, v):
        i -= 1
        j -= 1
        if not self._m.has_key(i):
            self._m[i] = {}
        if not self._m[i].has_key(j):
            self._m[i][j] = {}
        self._m[i][j] = v

    def __str__(self):
        s = self.simName + '\n'
        for i in range(self._N):
            s += '\t'
            for j in range(self._N):
                s += '%8.4f' % self._m[i][j]
            s += '\n'
        return s

def read_sim_file(files, fname):
    """
    Read filename, output similarity matrix.
    """
    sm = SimMatrix(fname)
    sm.init_from_files(files)
    with open(OUTPUTSDIR + fname, 'r') as f:
        line = f.readline()
        while line:
            line = f.readline()[:-1]
            if not line:
                break
            content = line.split(';')
            sm.set(int(float(content[0])), int(float(content[1])), float(content[2]))
    return sm

def read_files():
    docs = {}
    with open(OUTPUTSDIR + 'DOCS', 'r') as f:
        line = f.readline()
        i = 1
        while line:
            line = f.readline()[:-1]
            if not line:
                break
            docs[i] = line[1:-1]
            i += 1
    return docs

def main():
    files = read_files()
    sims = {}
    sims['MMMED'] = read_sim_file(files, 'MMMED')
    sims['NumCos'] = read_sim_file(files, 'NumCos')
    sims['NumDicS'] = read_sim_file(files, 'NumDicS')
    sims['NumED'] = read_sim_file(files, 'NumED')
    sims['NumIPS'] = read_sim_file(files, 'NumIPS')
    sims['NumJacc'] = read_sim_file(files, 'NumJacc')
    sims['NumKED_dot'] = read_sim_file(files, 'NumKED_dot')
    sims['NumKED_r'] = read_sim_file(files, 'NumKED_r')
    sims['NumMPS'] = read_sim_file(files, 'NumMPS')
    sims['NumOS'] = read_sim_file(files, 'NumOS')
    print files
    for v in sims.values():
        print v

if __name__ == '__main__':
    main()
