#!/usr/bin/env python

import sys, os, traceback, argparse, textwrap
from csv import DictReader


class FileCounts:

    def __init__(self, opts):
        self.data = dict()
        self.fieldnames = opts.fieldnames

        for field in self.fieldnames:
            self.data.setdefault(field, {})

    def add( self, line ):
        for field in self.fieldnames:

            value = line[field]

            self.data[field].setdefault(value, 0)
            self.data[field][value] += 1

    def sort_data( self ):

        for field in self.fieldnames:
            self.data[field] = sorted(self.data[field].items(), key=lambda item: item[1], reverse=True)

    def get_data( self ):

        self.sort_data()

        max_lines = max([len(self.data[key]) for key in self.data.keys()])

        if max_lines > 100:
            max_lines = 100

        return [ max_lines, self.data ]



class TheCount:

    def __init__(self, opts):
        self.options = opts
        self.files = opts.file

    def write( self, filedata):
            max_lines = filedata[0]
            data = filedata[1]
            idxlen = []

            print '\t'.join(self.fieldnames)
            for rowidx in range(max_lines):
                rowdata = []

                for i, field in enumerate(self.fieldnames):
                    try:
                        idxdata = data[field][rowidx]
                        idxlendata = len(str(idxdata[1]))

                        if rowidx == 0:
                            idxlen.append(idxlendata)

                        spacediff = idxlen[i] - idxlendata

                        rowdata.append('{} | {}'.format(str(idxdata[1]).rjust(idxlendata + spacediff), idxdata[0]))

                    except IndexError:
                        rowdata.append('')
                print '\t'.join(rowdata)


    def read( self, file ):

        with open(file, 'r') as f:

            dfile = DictReader(f, delimiter="\t")
            self.fieldnames = dfile.fieldnames

            filecounts = FileCounts(self.options)

            for line in dfile:
                filecounts.add(line)

            self.write( filecounts.get_data() )

    def main( self ):
        for file in self.files:
            self.read(file)
            break


def options():
    parser = argparse.ArgumentParser(
        description=textwrap.dedent( '''''' ),
        add_help=False,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument( '--help', help=argparse.SUPPRESS, action='help' )
    parser.add_argument( '-l', '--length', help="Max number of rows to output", type=int )
    parser.add_argument( '-h', '--headers', help="Comma delimited list of headers", type=str )
    parser.add_argument( 'file', help='File to parse', type=str, nargs="+" )

    return parser.parse_args( )


if __name__ == '__main__':
    try:
        main = TheCount( options() )
        sys.exit( main.main() )
    except KeyboardInterrupt, e:
        raise e
    except SystemExit, e:
        raise e
    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)