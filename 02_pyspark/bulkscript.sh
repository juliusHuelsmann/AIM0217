#!/bin/sh

# fail for not causing any tears
set -e


ls ../01_exploreData/out/check/
touch ../01_exploreData/out/check/t.csv
touch ../01_exploreData/out/check/bulkk
rm ../01_exploreData/out/check/*.csv
rm ../01_exploreData/out/check/bulk* -rf


for k in `seq 1 10`;
do
  
  # move stuff
  echo " creating dir ../01_exploreData/out/check/bulk$k"
  mkdir "../01_exploreData/out/check/bulk$k"


  # execute the program
  spark-submit main2.py $k 

  # move output 
  mv ../01_exploreData/out/check/*.csv "../01_exploreData/out/check/bulk$k/"

done
