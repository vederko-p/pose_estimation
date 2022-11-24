. utils.sh

OUTPUT_DIR="../src/weights"

weights_files_ids=(
  1X17CVDdgBSDWk4pMxhYf3aoreiY2014I
  1W-XQ9yVt6xtB0NgCzdjsR40II1plmQFH
)

weights_names=(
  yolov7_detector
  yolov7_pose_estimation
)

download_from_google_drive $OUTPUT_DIR $weights_files_ids $weights_names
