#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
#                   GNU GENERAL PUBLIC LICENSE
#                       Version 2, June 1991
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING.  If not, write to
# the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# 
#
#  2017.09.07      created by {user}
#
import sys
import os
import re
import getopt
import glob
import sqlite3

# TODO
# auto match for keyboard typo
TYPO_MAP = {
    'a': [],
    'b': [],
    'c': [],
    'd': [],
    'e': [],
    'f': [],
    'g': [],
    'h': [],
    'i': [],
    'j': [],
    'k': [],
    'l': [],
    'm': [],
    'n': [],
    'o': [],
    'p': [],
    'q': [],
    'r': [],
    's': [],
    't': [],
    'u': [],
    'v': [],
    'w': [],
    'x': [],
    'y': [],
    'z': [],
}

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: %s google_english.txt' % sys.argv[0])
        sys.exit(-1)

    f = open(sys.argv[1])
    d = f.read()
    f.close()

    
    groups = {}
    lines = d.splitlines()
    pattern = re.compile(r'^\W+|\W+$')
    for line in lines:
        if len(line) == 0:
            continue
        k = pattern.sub('', line)
        n = len(k)
        if n == 0:
            continue

        if n not in groups:
            groups[n] = []
        groups[n].append(k)

    fn = '%s.db' % (os.path.splitext(sys.argv[1])[0])
    if os.path.exists(fn):
        os.remove(fn)
    db = sqlite3.connect(fn)
    cur = db.cursor()
    cur.execute('CREATE TABLE eng_list(phrase TEXT, freq INTEGER, len INTEGER, c0 TEXT, c1 TEXT, c2 TEXT, c3 TEXT, c4 TEXT)')

    for k_len in sorted(groups):
        print(k_len, len(groups[k_len]))
        for k in groups[k_len]:
            params = [k, k_len];
            for i in range(5):
                if i < k_len:
                    params.append(k[i])
                else:
                    params.append('')
            cur.execute('INSERT INTO eng_list(phrase, freq, len, c0, c1, c2, c3, c4) VALUES(?, 0, ?, ?, ?, ?, ?, ?)', params)

    db.commit()

        




