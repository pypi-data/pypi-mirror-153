#!/usr/bin/python
from pyvirtualdisplay import Display
import os
display = Display(visible=0, size=(1280, 1024))
display.start()

from mayavi import mlab

def main(argv):
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-o", "--output", type="str", dest="output", help="output animation name")
    parser.add_option("-m", "--min", type="float", default=None, dest="min", help="min value in color scale")
    parser.add_option("-M", "--max", type="float", default=None, dest="max", help="max value in color scale")
    parser.add_option("-g", "--gbif", type="string", default=None, dest="gbif", help="Occurence file gotten from get_gbif")
    parser.add_option("-w", "--warp-scale", type="float", default=1.0, dest="warp_scale", help="Warp scale for the vertical axis.")
    parser.add_option("-t", "--triangles", type="int", default=None, dest="nb_triangles", help="Number of triangles for the delaunay tiangulation if -g is defined")
    parser.add_option("--DDD", dest="DDD", default = False, action = 'store_true', help="Plot a 3 dimensional version of the data")
    parser.add_option("--no-DDD", dest="DDD", action = 'store_false', help="Normal 2 dimension plot.")
    (options, args) = parser.parse_args(argv)
    return chose_method(args[0],
     vmin=options.min,
     vmax=options.max,
     output=options.output,
     gbif_occurrences=options.gbif,
     DDD=options.DDD,
     warp_scale=options.warp_scale,
     nb_triangles=options.nb_triangles
     )

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
