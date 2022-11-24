. utils.sh

UTPUT_DIR="../src/weights"

default_data_files_ids=(
  1wuKA6OQNd7xEKJ1zzkBz-0NffSClwrdy
  1GEBJDNXZyB3MYqUi2OXYc6xk0nQZ7-O6
)

default_data_names=(
  yolov7_detector
  yolov7_pose_estimation
)

download_from_google_drive $OUTPUT_DIR $default_data_files_ids $default_data_names
