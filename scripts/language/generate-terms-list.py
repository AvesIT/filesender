#!/usr/bin/env python3

# This generates a terms list in txt and json format
# txt is used for backward compatibility
# json is used for import into poeditor project for filesender 3+

import os
import re
import json
import sys

lang_term_re = r'\$lang\[\'(.*)\'\].*'
lang_file_re = r'(.*)\.(.*)\.php'

valid_contexts = ['mail', 'text', 'html']
terms = list()
termlist = set()

LANGTREE = "../../language/"

DEBUG = False

if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} <directory>')
    print('<directory> specifies where to store terms.txt and terms.json')
    exit(1)

if not os.path.isdir(sys.argv[1]):
    print(f'Usage: {sys.argv[0]} <directory>')
    print(f'Directory {sys.argv[1]} does not exist. Please create it')
    exit(2)

destdir = sys.argv[1]

# Walk language tree
for root, d_names, f_names in os.walk(LANGTREE):
    if DEBUG: print(f'In {root}')

    for fn in f_names:

        # Parse lang.php
        if fn == 'lang.php':
            if DEBUG: print(f'Found lang.php in {root}/{fn}') 

            fh = open(root + '/' + fn, "r")
            for line in fh.readlines():
                re_search = re.search(lang_term_re, line)
                if re_search and re_search.group(1) is not None and re_search.group(1) not in termlist:
                    if DEBUG: print(f'Found term {re_search.group(1)}')
                    terms.append({'term': re_search.group(1)})
                    termlist.add(re_search.group(1))
            fh.close()

        elif any(ctx in fn for ctx in valid_contexts):
        
            if DEBUG: print(f'Found valid file in {root}/{fn}')
            

            re_search = re.search(lang_file_re, fn)

            if re_search and re_search.group(1) is not None and re_search.group(2) is not None and re_search.group(1) not in termlist:
                if DEBUG: print(f'Found term {re_search.group(1)}')
                terms.append({'term': re_search.group(1),'context': re_search.group(2)})
                termlist.add(re_search.group(1))


sorted_termlist = sorted(termlist)

fh_terms = open( destdir + 'terms.txt', 'w')
fh_termsjson = open(destdir + 'terms.json', 'w')

for term in sorted_termlist:
    fh_terms.write(term)
    fh_terms.write('\n')

json.dump(terms, fh_termsjson, indent=4)
