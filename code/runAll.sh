#!/bin/bash

usage () {
    echo "$0 OUTDIR FILE1 FILE2 FILE3 ...."
    exit 1
}

if [ $# -lt 3 ]; then
    usage
fi

OUTDIR=$1
shift
FILES=$@

[ -d $OUTDIR ] || usage

for i in $FILES; do
    [ -f $i ] || usage
done

# build code dirs (to be ignored anyway)
BUILD_DIR="tcase"
[ -d "$BUILD_DIR" ] || mkdir "$BUILD_DIR"
INPUT_DIR="$BUILD_DIR""/inputs"
[ -d "$INPUT_DIR" ] || mkdir "$INPUT_DIR"
OUTPUTSDIR="$BUILD_DIR""/outputs"
[ -d "$OUTPUTSDIR" ] || mkdir "$OUTPUTSDIR"
TREEDIR="$BUILD_DIR""/trees"
[ -d "$TREEDIR" ] || mkdir "$TREEDIR"
HEATDIR="$BUILD_DIR""/heatmaps"
[ -d "$BUILD_DIR" ] || mkdir "$BUILD_DIR"

# copy files to $INPUT_DIR
cp $@ "$INPUT_DIR"

# run RM cli.
./RMcli.sh RM.rmp

# parse results
./parse_results.py
