#! /bin/sh

export SLURM_ACCOUNT=rubin:commissioning
export SALLOC_ACCOUNT=$SLURM_ACCOUNT
export SBATCH_ACCOUNT=$SLURM_ACCOUNT
export SLURM_PARTITION=roma,milano
