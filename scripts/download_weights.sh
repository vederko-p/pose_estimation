. utils.sh

OUTPUT_DIR="../src/weights"

weights_files_ids=(
  1wuKA6OQNd7xEKJ1zzkBz-0NffSClwrdy
  1GEBJDNXZyB3MYqUi2OXYc6xk0nQZ7-O6
)

weights_names=(
  yolov7_detector
  yolov7_pose_estimation
)

download_from_google_drive $OUTPUT_DIR $weights_files_ids $weights_names
