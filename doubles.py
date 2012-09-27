#!/usr/bin/python
"""A script detecting double words and double word pairs in a text.
   
THIS CODE IS IN PUBLIC DOMAIN

Original author: Slawek Ligus
"""
import os
import re
import optparse

RED = '\x1b[1;31m'
NORMAL = '\033[0m' 

# Tests
DOUBLE_WORD = re.compile(r'\b(\w+) \1\b')
DOUBLE_PAIR = re.compile(r'\b(\w+) (\w+) \1 \2\b')

def scan_for_duplicates(filename, color=True):
    """Scan file for duplicate line entries."""
    for (line_no, line) in enumerate(open(filename)):
        for test in (DOUBLE_WORD, DOUBLE_PAIR):
            search_result = test.search(line)
            if search_result:
                repeated = test.search(line).group()
                snippet = line.strip()
                if color:
                    color_repeated = RED + repeated + NORMAL
                    snippet = snippet.replace(repeated, color_repeated)
                print '%12s line %2i: %s' % (filename, line_no + 1, snippet)

if __name__ == "__main__":
    oparser = optparse.OptionParser(usage='%prog [options] <file1> ...')
    oparser.add_option('-n', '--no-color', action='store_false', dest='color',
                    default=True, help="Don't emphasize the phrase with color.")
    opts, args = oparser.parse_args()
    if len(args) < 1:
        oparser.error('Specify a file to scan,')
     
    for filename in args:
        if os.path.isfile(filename):
            scan_for_duplicates(filename, opts.color)
