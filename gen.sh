#!/bin/bash

types=(UU UW VX SX UX WW WX XX RR SS TT UU VV WW XX)

for t in ${types[@]}
do
    ./encode.py $t > $t.cnf
    md5sum $t.cnf
done
