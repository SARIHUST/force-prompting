# this is our pretrained model; you can change to your own path
CHECKPOINT="checkpoints/step-5000-checkpoint-point-force.pt"

# you can change this to the list of csvs you want to run inference on.
IMAGE_CSVS=(
  "/projects/vig/hhwang/PhysVideoGen/inference_dataset/point-force/test/custom/point-force.csv"
)

for image_csv in "${IMAGE_CSVS[@]}"; do
  bash scripts/inference_1_gpu.sh \
      --force_type "point_force" \
      --model_type "controlnet_with_force_control_signal" \
      --num_validation_videos 1 \
      --csv_path_val "${image_csv}" \
      --pretrained_controlnet_path "${CHECKPOINT}" \
      --output_dir "inference-point-force"
done