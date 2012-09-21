#!/usr/bin/python

"""A script generating figure list meeting ORM illustrations guidelines.
http://oreillynet.com/oreilly/authors/welcome/illustrations.csp
   
THIS CODE IS IN PUBLIC DOMAIN

Original author: Slawek Ligus
"""

import csv
import os
import optparse
import xml.etree.ElementTree as ET

XMLNS = 'http://www.w3.org/2001/XInclude'


class FigureProcessor(object):

    """ORM Manuscript Figure List processor."""

    def __init__(self, filename, outfile='/dev/stdout'):
        """Construct FigureProcessor."""
        self.chapter = 0
        self.figure = 0
        self.filename = filename
        self.outfile = outfile
        self.dirname = os.path.dirname(filename) or '.'
        self.in_appendix = False
        self.csv = None

    def process(self):
        """Create a CSV figure list."""
        bookroot = ET.ElementTree(file=self.filename).getroot()
        booktitle = bookroot.find('title').text
        self.csv = csv.writer(open(self.outfile, 'w'), delimiter=',')
        self.csv.writerow([booktitle])
        self.csv.writerow(['Fig#', 'Filename', 'Caption', 'Type'])
        for include in bookroot.findall('{%s}include' % XMLNS):
            self._process_chapter(include)

    def _process_chapter(self, include):
        """Parse the cross-referenced chapter for figures."""
        chapter_file = self.dirname + '/' + include.attrib['href']
        chaproot = ET.ElementTree(file=chapter_file).getroot()
        if chaproot.tag == 'chapter':
            self.chapter += 1
        elif chaproot.tag == 'appendix':
            if not self.in_appendix:
                self.in_appendix = True
                self.chapter = 0
            self.chapter += 1

        self.figure = 0
        for element in chaproot.getiterator():
            if element.tag == 'figure':
                self._process_figure(element)

    def _process_figure(self, figure):
        """Extract information from the figure element."""
        self.figure += 1
        title, content = tuple(figure)

        if content.tag == 'screenshot':
            img_type = 'Screenshot'
            mediaobj = content.find('mediaobject')
        else:
            img_type = 'Drawing'
            mediaobj = content

        imgdata = mediaobj.find('imageobject').find('imagedata')
        imgfile = os.path.basename(imgdata.attrib.get('fileref', ''))

        fignum = '%i-%i' % (self.chapter, self.figure)
        if self.in_appendix:
            fignum = '%s-%i' % (chr(ord('A') - 1 + self.chapter), self.figure)
        # Remove whitespace and replace unicode characters (not handled by csv).
        norm_text = ' '.join(title.text.split()).encode('ascii', 'replace')
        self.csv.writerow([fignum, imgfile, norm_text, img_type])
        
        
if __name__ == "__main__":
    oparser = optparse.OptionParser(usage='%prog [options] <book.xml>')
    oparser.add_option('-o', '--output', dest='outfile', default='/dev/stdout',
                       help='write figure list to FILE', metavar='FILE')
    opts, args = oparser.parse_args()
    if len(args) != 1:
        oparser.error('Incorrect number of arguments: %i' % len(args))
     
    figproc = FigureProcessor(args[0], outfile=opts.outfile)
    figproc.process()
