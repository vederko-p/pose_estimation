. utils.sh

# Download standard dataset

OUTPUT_DIR="../data"

default_data_files_ids=(
  1_EBIS3Sl8rfcst1OsruT7O1GK-2wb1Fd
)

default_data_names=(
  first_test_data
)

download_from_google_drive $OUTPUT_DIR $default_data_files_ids $default_data_names
