#!/bin/bash
#SBATCH --partition=ct,sharedp
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --job-name=finetune_wind_force_change
#SBATCH --output=slurm-logs/output.%N.%x.%j.log
#SBATCH --error=slurm-logs/error.%N.%x.%j.log
#SBATCH --gres=gpu:h100:4
#SBATCH --account=ct
#SBATCH --requeue

source activate force-prompt

export WANDB_MODE=offline

bash scripts/train_4_gpu.sh \
    --force_type "wind_force_change" \
    --video_root_dir "datasets/wind-force-change/wind_force_change_15000" \
    --csv_path "datasets/wind-force-change/wind_force_change_15000.csv"