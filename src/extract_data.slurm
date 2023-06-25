#!/bin/bash

#SBATCH -N 1 

#SBATCH -c 1 

#SBATCH --mem=8gb

#SBATCH --time=0-00:15:00

#SBATCH --output=my.stdout 

#SBATCH --mail-user=dxk912@case.edu

#SBATCH --mail-type=ALL 

#SBATCH --job-name="extract metadata"

module load Python/3.8.6-GCCcore-10.2.0
module load FFmpeg/4.3.1-GCCcore-10.2.0
conda create --name Semantic
conda activate Semantic

conda install pillow
pip install open-clip-torch
pip install sentence-transformers

cd Semantic-search-in-video-datasets

cp -r . $PFSDIR

cd $PFSDIR

python3 src/extarct_data_all_files.py vrt_files/ output_data/

rm -rf "$PFSDIR"/*

cp -ru * $SLURM_SUBMIT_DIR
