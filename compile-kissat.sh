#!/bin/bash
if [ ! -d kissat ]
then
	git clone git@github.com:arminbiere/kissat.git
fi
cd kissat
if [ ! -f makefile ]
then
	./configure
fi
make -j
cd "$OLDPWD"
