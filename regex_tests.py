#!/usr/bin/python
"""A set of naive, regex-based lexical tests for detecting common mistakes.
   
THIS CODE IS IN PUBLIC DOMAIN

Original author: Slawek Ligus
"""
import os
import re
import optparse

RED = '\x1b[1;31m'
NORMAL = '\033[0m' 

TESTS = {
    'double word': re.compile(r'\b(\w+) \1\b'),
    'double word pair': re.compile(r'\b(\w+) (\w+) \1 \2\b'),
    "incorrect use of \"it's\"": re.compile(r'\b(through|with|for) it.s\b'),
    "incorrect use of 'its'": re.compile(r'\bits a\b'),
}
def scan_for_duplicates(filename, color=True):
    """Scan file for duplicate line entries."""
    try:
        for (line_no, line) in enumerate(open(filename)):
            for reason, test in TESTS.iteritems():
                search_result = test.search(line)
                if search_result:
                    repeated = test.search(line).group()
                    snippet = line.strip()
                    if color:
                        color_repeated = RED + repeated + NORMAL
                        snippet = snippet.replace(repeated, color_repeated)
                    print '%12s, line %2i: %s (%s)' % (filename, line_no + 1,
                                                       snippet, reason)
    except IOError, err:
        print err
        
if __name__ == "__main__":
    oparser = optparse.OptionParser(usage='%prog [options] <file1> ...')
    oparser.add_option('-n', '--no-color', action='store_false', dest='color',
                    default=True, help="Don't emphasize the phrase with color.")
    opts, args = oparser.parse_args()
    if len(args) < 1:
        oparser.error('Specify a file to scan,')
     
    for filename in args:
        scan_for_duplicates(filename, opts.color)
