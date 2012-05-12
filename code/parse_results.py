#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

OUTPUTSDIR='tcase/outputs/'
HEATDIR='tcase/heatmaps/'

class SimMatrix:
    def __init__(self, simName, eMax=False):
        self.simName = simName
        self._m = {}
        self._N = 0
        self._max = eMax

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
        return self.simName + '\n' + self.content() + '\n'

    def content(self):
        s = ''
        for i in range(self._N):
            s += '\t'
            for j in range(self._N):
                s += '%8.4f' % (self._m[i][j] if self._max else -self._m[i][j])
            s += '\n'
        return s[:-1]

def read_sim_file(files, fname, eMax=False):
    """
    Read filename, output similarity matrix.
    """
    sm = SimMatrix(fname, eMax)
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

def construct_sims(files):
    sims = {}
    sims['MMMED'] = read_sim_file(files, 'MMMED', False)
    sims['NumCos'] = read_sim_file(files, 'NumCos')
    sims['NumDicS'] = read_sim_file(files, 'NumDicS')
    sims['NumED'] = read_sim_file(files, 'NumED', False)
    sims['NumIPS'] = read_sim_file(files, 'NumIPS')
    sims['NumJacc'] = read_sim_file(files, 'NumJacc')
    sims['NumKED_dot'] = read_sim_file(files, 'NumKED_dot', False)
    sims['NumKED_r'] = read_sim_file(files, 'NumKED_r', False)
    sims['NumMPS'] = read_sim_file(files, 'NumMPS')
    sims['NumOS'] = read_sim_file(files, 'NumOS')
    return sims

def output(files, sims):
    print files
    for v in sims.values():
        print v

def heat_maps(files, sims):
    for k in sims.keys():
        heat = """
set term png
set key on
plot '-' matrix with image title "%s"
%s
e
e
        """ % (files, sims[k].content())
        with open("tmp", "w") as f:
            f.write(heat)
        os.system('gnuplot tmp > %s%s.png' % (HEATDIR, k))
    os.system('rm tmp')

def main():
    files = read_files()
    sims = construct_sims(files)
    output(files, sims)
    heat_maps(files, sims)

if __name__ == '__main__':
    main()
