#!/bin/bash

chemin="./data/dataset/"
for i in $chemin$1* ;
do
    # echo $i
    # echo $chemin${i#"./data/dataset/New"}
	# echo "\n"
    mv -v $i $chemin${i#"./data/dataset/New"}
done