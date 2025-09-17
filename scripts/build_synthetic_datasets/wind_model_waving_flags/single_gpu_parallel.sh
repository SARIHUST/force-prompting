#!/bin/bash
RENDER_SCRIPT="scripts/build_synthetic_datasets/wind_model_waving_flags/waving_flags_render.sh" # Blender script
NUM_PROCESSES=2

echo "Starting ${NUM_PROCESSES} concurrent processes."

for ((i=1; i<=NUM_PROCESSES; i++))
do
    sh "${RENDER_SCRIPT}" &
done

echo "All tasks submitted. Waiting for all to complete..."
wait
echo "All tasks ${NUM_PROCESSES} completed."