#!/usr/bin/python
#
##---------------------------------------------------------------------------
## Author:      Sean D'Epagnier
## Copyright:   
## License:     GPLv3+
##---------------------------------------------------------------------------
#

import sys
import os
import tempfile
import subprocess

# so we total lists with apply
def add(*args):
    if len(args):
        return args[0] + apply(add, args[1:])
    return 0

#regionfile = 'Regions/regions'
#outputdir = 'output'
#inputfiles = ['/home/sean/charts/nautical/9/C4500084.1.kap']

regionfile = sys.argv[1]
outputdir = sys.argv[2]
#inputfiles = sys.argv[3:]

inputfiles = sys.stdin.readlines()


regions = open(regionfile).readlines()

if not os.path.exists(outputdir):
   os.makedirs(outputdir)

for region in regions:
    name = region.split(' ')[0]
    
    outdir = outputdir+"/"+name
    if not os.path.exists(outdir):
        os.makedirs(outdir)

inputtotal = len(inputfiles)
inputcount = 0

for inputfile in inputfiles:
    inputfile = inputfile.rstrip()

    kapheader = tempfile.NamedTemporaryFile(suffix=".kap")
    temppng = tempfile.NamedTemporaryFile(suffix=".png")

    imgkapcommand = ["imgkap", inputfile, kapheader.name]
#    print ' '.join(imgkapcommand)
    if subprocess.call(imgkapcommand) != 0:
        print "imgkap failed, aborting"
        continue

    content = kapheader.readlines()

    prev = []
    headerlines = []
    # pre-parse header combining multilines
    for line in content:
        l = line.rstrip()
        if l[:4] == '    ':
            prev = prev + l.strip().split(',')
        else:
            if len(prev):
                headerlines.append(prev)
                prev = l.split(',')
                
    headerlines.append(prev)
    ply = []
    for l in headerlines:
        if len(l) > 0 and l[0][:3] == 'PLY':
            ply.append(map(float, l[1:]))

    copycount = 0
    percent = "%.1f%%" % (inputcount * 100.0 / inputtotal)
    for region in regions:
        sregion = region.rstrip().split(' ')
        name = sregion[0]
        def myzip(l):
            if len(l):
                return [[l[0], l[1]]] + myzip(l[2:])
            return []

        ll = myzip(sregion[1:])

        outdir = outputdir+"/"+name

        def ptinrgn(p):
            lpos = len(ll) - 1
            total = 0
            for pos in range(len(ll)):
                ll0 = map(float, ll[lpos])
                ll1 = map(float, ll[pos])
                if ll1[1] - ll0[1] > 180:
                    ll1[1] = ll1[1] - 360
                elif ll0[1] - ll1[1] > 180:
                    ll0[1] = ll0[1] - 360

                if (ll0[1] + ll1[1])/2 - p[1] > 180:
                    ll0[1] = ll0[1] - 360
                    ll1[1] = ll1[1] - 360                    
                elif p[1] - (ll0[1] + ll1[1])/2 > 180:
                    ll0[1] = ll0[1] + 360
                    ll1[1] = ll1[1] + 360                    

                a = ll1[0] - ll0[0], ll1[1] - ll0[1]
                b = p[0]+100, 0 # very far south
                c = ll0[0] - p[0], ll0[1] - p[1]
                d = a[1] * b[0] - a[0] * b[1]

                na = (b[1] * c[0] - b[0] * c[1]) / d
                if na > 0 and na <= 1:
                    nb = (a[0] * c[1] - a[1] * c[0]) / d
                    if nb > 0 and nb <= 1:
                        total = total + 1
                lpos = pos
            return total & 1
        
        if apply(add, map(ptinrgn, ply)) > 0: #len(ply)/2:
            copycount = copycount + 1

            outputfile = inputfile
            if outputfile[0] == '.':
                outputfile = outputfile[1:]
            outputfile = outdir + outputfile
            dir = os.path.dirname(outputfile)
            if not os.path.exists(dir):
                os.makedirs(dir)

            cpcommand = ["cp", inputfile, outputfile]
            print percent, ' '.join(cpcommand)
            if subprocess.call(cpcommand) != 0:
                print "cp failed, aborting"
                exit(1)

    if copycount == 0 and len(ply):
        print percent, inputfile, "belongs to no regions", ply
    if copycount > 2:
        print percent, inputfile, "belongs to multiple regions"

    inputcount = inputcount + 1
