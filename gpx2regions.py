#!/usr/bin/python
#
##---------------------------------------------------------------------------
## Author:      Sean D'Epagnier
## Copyright:   
## License:     GPLv3+
##---------------------------------------------------------------------------
#
# convert gpx to regions file
#

import sys
import xml.etree.ElementTree

e = xml.etree.ElementTree.fromstring(sys.stdin.read())
for path in e.iter('{http://www.opencpn.org}path'):
    line = path.find('name').text
    # o-draw doubles the first and last coords to define a loop
    for p in path.findall("{http://www.opencpn.org}ODPoint")[1:]:
        line = line + " " + p.attrib['lat'] + " " + p.attrib['lon']
    print line
