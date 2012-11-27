#!/bin/bash

#shell script for statistics creation. This shell script generates a table of
#statistics for a lot of happiness thresholds and saves them into happiness.csv

STATFILE=stats.csv

#set numeric locale to C in order to get correct separators
LC_NUMERIC=C

#search space
START=0.0
STEP=0.01
END=1.0
DAYS=1000000

SIM=./stats

rm -f $STATFILE

#main loop
for i in $(seq $START $STEP $END)
do
	{ echo -n "$i," ; $SIM $DAYS $i ; } >>$STATFILE
done
