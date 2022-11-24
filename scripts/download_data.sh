# Download standard dataset

OUTPUT_DIR="../data"

default_data_files_ids=(
  1pVXgseThE0qA2zcVtkjIDceLzS2f23mA
)

default_data_names=(
  first_test_data
)

check_and_mkdir $OUTPUT_DIR
cd $OUTPUT_DIR


for i in ${!default_data_files_ids[*]}
do
  file_id=${default_data_files_ids[i]}
  file_name=${default_data_names[i]}
  echo Download $file_name dataset...
  gdown $file_id
  unzip "$file_name.zip" -d $file_name
  rm "$file_name.zip"
done
