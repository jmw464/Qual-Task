#!/bin/bash
#SBATCH -n 2
#SBATCH --job-name=eff
#SBATCH --qos=regular
#SBATCH -C haswell
#SBATCH --time=3:59:00
#SBATCH --error=jobs/eff_%j.err
#SBATCH --output=jobs/eff_%j.out

python scripts/find_reweighting.py
