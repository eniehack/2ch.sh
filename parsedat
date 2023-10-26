#!/bin/sh

awk -F'<>' '{ print NR,$1, $2, $3,"\n",$4,"\n" }' | sed 's/<br>/\n/g'
