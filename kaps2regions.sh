#!/bin/bash

time find | grep kap | /usr/local/bin/kapsort.py /usr/local/share/kapsort/regions output

#cd output
#for i in *; do echo $i; tar cJf $i.tar.xz $i; rm -rf $i; done
