#!/bin/bash
#SBATCH --job-name=PostProcessing
#SBATCH --nodes=1
#SBATCH --cpus-per-task=5
#SBATCH --mem=50g
#SBATCH --time=96:00:00
#SBATCH --account=mdcoll0
#SBATCH --partition=standard
#SBATCH --mail-type=BEGIN,END,FAIL

module load python3.10-anaconda/2023.03

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

python read_data.py
python organize_data.py

