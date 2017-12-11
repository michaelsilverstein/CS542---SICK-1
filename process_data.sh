#!/bin/bash -l

#$ -P cs542/SICK1

#$ -l h_rt=12:00:00

#$ -m e

#$ -N Data Process Script

#$ -j y

module load python/3.6.2

for file in /projectnb/cs542/SICK1/Data/*.xml;
do python preprocess.py $file /projectnb/cs542/SICK1/Processed_data;
done
