#!/bin/bash

#shell script for statistics creation. This shell script generates a table of
#statistics for a lot of happiness thresholds and saves them into happiness.csv

#various parameters
STATFILE=stats.tsv
SIM=./stats
JOBS=$(grep -ic ^processor /proc/cpuinfo) #number of processors available

#search space
START=0.0
STEP=0.0016
END=0.5
DAYS=$((1024*1024))

LC_NUMERIC=C #set numeric locale to C in order to get correct separators
LC_COLLATE=C #set collating sequence to C in order to sort correctly
#calculate results in parallel
seq $START $STEP $END | xargs -n 1 -P $JOBS $SIM $DAYS >$STATFILE
sort -o $STATFILE $STATFILE #sort output as it might be unordered
