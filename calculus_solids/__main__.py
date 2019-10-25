from .plotting_math import *

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('solid', help='''choose the solid to produce:
REVOLUTION - for a solid of revolution
CROSS_SQUARE - for a solid with square/rectangular cross sections
CROSS_TRIANGLE - for a solid with triangular cross sections
CROSS_SEMICIRCLE - for a solid with semi circle cross sections''')

parser.add_argument('-f1','--function1',type=str,help='the upper function to graph')
parser.add_argument('-f2','--function2',type=str,help='the lower function to graph')

parser.add_argument('-l','--lower',type=float,help='the lower limit of the integral',required=True)
parser.add_argument('-u','--upper',type=float,help='the upper limit of the integral',required=True)

parser.add_argument('-p','--precision',type=float,help='the smallest increment between x-values. [default: 0.1]',default=0.1)
parser.add_argument('-y','--y-offset',type=float,help='(solid of revolution only), horizontal line to revolve around, [default: y=0]', default=0)

parser.add_argument('-i','--invert',action='store_true',help='faces of solids will be inverted inside out. Might fix appearance issues')

parser.add_argument('-W','--wireframe',action='store_true',help='no faces will be calculated, may cause many issues')
parser.add_argument('-B','--basic',action='store_true',help='only vertices will be calculated, may cause many issues')

parser.parse_args("".split())
parser.parse_args("".split())
parser.parse_args("".split())