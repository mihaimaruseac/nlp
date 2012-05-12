#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

OUTPUTSDIR='tcase/outputs/'
HEATDIR='tcase/heatmaps/'
TREEDIR='tcase/trees/'
eps = .1
MAX = -42424242
MIN = 42424242

class SimMatrix:
    def __init__(self, simName, eMax=True):
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
        if (not self._max) and i != j:
            v = 1.0 / (eps + v)
        self._m[i][j] = v

    def __str__(self):
        return self.simName + '\n' + self.content() + '\n'

    def content(self, hmap=False):
        _f_ = lambda x: x
        if hmap:
            m, M = MIN, MAX
            for i in range(self._N):
                for j in range(self._N):
                    m = min(m, self._m[i][j])
                    M = max(M, self._m[i][j])
            if m != M:
                _f_ = lambda x: (x - m) / (M - m)
        s = ''
        for i in range(self._N):
            s += '\t'
            for j in range(self._N):
                s += '%8.4f' % _f_(self._m[i][j])
            s += '\n'
        return s[:-1]

    def _compute_adj(self):
        adj = []
        for i in range(self._N):
            for j in range(i + 1, self._N):
                adj.append((i, j, self._m[i][j]))
        adj.sort(cmp=lambda x,y: 1 if x[2] < y[2] else -1 if x[2] > y[2] else 0)
        return adj

    def compute_apm(self):
        apm = []
        adj = self._compute_adj()
        connecteds = {}
        for i in range(self._N):
            connecteds[i] = i
        na = self._N - 1
        while na > 0:
            i, j, c = adj[0]
            if connecteds[i] != connecteds[j]:
                v = min(connecteds[i], connecteds[j])
                connecteds[i] = v
                connecteds[j] = v
                na -= 1
            apm.append((i, j, c))
            adj = adj[1:]
        return apm

def read_sim_file(files, fname, eMax=True):
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
    for k in sims:
        heat = """
set term png
set key on
plot '-' matrix with image title "%s"
%s
e
e
        """ % (files, sims[k].content(hmap=True))
        with open('%s%s' % (HEATDIR, k), 'w') as f:
            f.write(heat)
        os.system('gnuplot %s%s > %s%s.png' % (HEATDIR, k, HEATDIR, k))

def trees(files, sims):
    for k in sims:
        apm = sims[k].compute_apm()
        s = 'graph %s {\n' % k
        for i, j, c in apm:
            s += '\t%s -- %s [label=%5.3f];\n' % (files[i + 1], files[j + 1], c)
        s += '}'
        with open('%s%s.dot' % (TREEDIR, k), 'w') as f:
            f.write(s)
        os.system('dot -Tpng %s%s.dot > %s%s.png' % (TREEDIR, k, TREEDIR, k))

def main():
    files = read_files()
    sims = construct_sims(files)
    output(files, sims)
    heat_maps(files, sims)
    trees(files, sims)

if __name__ == '__main__':
    main()
