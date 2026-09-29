#!/bin/zsh
# usage: flowshots.sh OUTPREFIX MODE STEPS 'json params' ...
out=$1; mode=$2; shift 2; i=0
for spec in "$@"; do steps=${spec%%|*}; p=${spec#*|}; enc=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$p")
  node pageshot.mjs "file:///Users/boxer/ben-advice/soap-films/tools/flowtest.html?mode=$mode&steps=$steps&p=$enc" ${out}_$i.jpg 200 640 640 | grep -v "no errors"; i=$((i+1)); done
