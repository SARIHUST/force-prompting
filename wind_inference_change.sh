# this is our pretrained model; you can change to your own path
CHECKPOINT="output/wind_force_change/2025-09-19_20-31-16/step-3000-checkpoint.pt"

# you can change this to the list of csvs you want to run inference on.
IMAGE_CSVS=(
  "inference_dataset/wind-force/test/custom/merged_benchmark.csv"
)

for image_csv in "${IMAGE_CSVS[@]}"; do
  bash scripts/inference_1_gpu.sh \
      --force_type "wind_force_change_inference" \
      --model_type "controlnet_with_force_control_signal" \
      --num_validation_videos 1 \
      --csv_path_val "${image_csv}" \
      --pretrained_controlnet_path "${CHECKPOINT}" \
      --output_dir "" 
done