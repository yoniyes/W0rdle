#!/bin/zsh
for (( i=0; i < 2000; i++ )) do; echo $(python3 ./solver.py); done | grep 'YOU WON' | wc -l | perl -ne 'chomp; s/^\s*(.*)\s*$/$1/; print "Success rate = ".(100*$_/2000)."%\n"'