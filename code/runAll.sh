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

BUILD_DIR="tcase"
INPUT_DIR="$BUILD_DIR""/inputs"
OUTPUTSDIR="$BUILD_DIR""/outputs"
TREEDIR="$BUILD_DIR""/trees"
HEATDIR="$BUILD_DIR""/heatmaps"

RESULTS="aggregated-results"
HMAPS="aggregated-heatmap.png"
TREES="aggregated-trees.png"

[ -d $OUTDIR ] || usage

for i in $FILES; do
    [ -f $i ] || usage
done

# build code dirs (to be ignored anyway)
[ -d "$BUILD_DIR" ] || mkdir "$BUILD_DIR"
[ -d "$INPUT_DIR" ] || mkdir "$INPUT_DIR"
[ -d "$OUTPUTSDIR" ] || mkdir "$OUTPUTSDIR"
[ -d "$TREEDIR" ] || mkdir "$TREEDIR"
[ -d "$HEATDIR" ] || mkdir "$HEATDIR"

# copy files to $INPUT_DIR
cp $@ "$INPUT_DIR"

# run RM cli.
echo "Mining data..."
./RMcli.sh RM.rmp

# parse results
echo -e "\nParsing results...."
./parse_results.py > "$OUTDIR"/"$RESULTS"

# Aggregate data
echo -e "\nAgreggating data...."
montage -geometry 1024x768 "$TREEDIR"/*.png "$OUTDIR"/"$TREES"
montage -geometry 1024x768 "$HEATDIR"/*.png "$OUTDIR"/"$HMAPS"

# Done
echo -e "\nFinished everything. See content of $OUTDIR"
