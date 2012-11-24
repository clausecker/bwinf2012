#!/usr/bin/env python

# check for python 3!
import sys
if sys.version_info[0] < 3:
	print("This program needs at least Python 3 to run.")
del sys


# actual program
def iterate(processor, in_file, out_file):
	processor(in_file, out_file).start()

if __name__ == '__main__':
	import argparse
	import sys

	from sierpinsky import SierpinskyProcessor

	p = argparse.ArgumentParser()
	p.add_argument('input', nargs='?', default='-',
		help="file to use as input (default: stdin)")
	p.add_argument('output', nargs='?', default='-',
		help="file to output to (default: stdout)")
	args = p.parse_args()

	in_file = sys.stdin
	out_file = sys.stdout

	if args.input != '-':
		in_file = open(args.input, 'r')
	if args.output != '-':
		out_file = open(args.output, 'w')

	iterate(SierpinskyProcessor, in_file, out_file)

	in_file.close()
	out_file.close()

