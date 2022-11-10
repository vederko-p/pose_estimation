# Download standard dataset

OUTPUT_DIR="../data"

default_data_files_ids=(
  1MyOyXlt-57IylUJm4tpVJiogXute6e40
)

default_data_names=(
  first_test_data
)

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
