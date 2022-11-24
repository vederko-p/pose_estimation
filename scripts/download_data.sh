. utils.sh

# Download standard dataset

OUTPUT_DIR="../data"

default_data_files_ids=(
  1pVXgseThE0qA2zcVtkjIDceLzS2f23mA
)

default_data_names=(
  first_test_data
)

download_from_google_drive $OUTPUT_DIR $default_data_files_ids $default_data_names
