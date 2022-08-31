#!/bin/bash
#SBATCH -n 2
#SBATCH --job-name=eff
#SBATCH --qos=regular
#SBATCH -C haswell
#SBATCH --time=3:59:00
#SBATCH --error=jobs/eff_%j.err
#SBATCH --output=jobs/eff_%j.out

WP=0.60 #choose between 0.60, 0.70, 0.77 and 0.85
XVAR=eta #choose between pt_high, pt_low and eta

python scripts/compute_efficiencies.py -w ${WP} -v ${XVAR}
