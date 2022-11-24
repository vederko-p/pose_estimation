check_and_mkdir() {
  local dirname=$1
  if [[ ! -d $dirname ]]
  then
    mkdir $dirname
  fi
}


install_requirements() {
  local directory=$1
  local recs_filename="requirements.txt"

  cd $directory
  if [[ -f $recs_filename ]]
  then
    pip install -r $recs_filename
    cd -
  fi
}


download_from_google_drive() {
  local output_dir=$1
  local files_ids=$2
  local files_names=$3

  check_and_mkdir $output_dir
  cd $output_dir

  for i in ${!files_ids[*]}
  do
    local file_id=${files_ids[i]}
    local file_name=${files_names[i]}
    echo Download $file_name...
    gdown $file_id
    unzip "$file_name.zip" -d $file_name
    rm "$file_name.zip"
  done

  cd -
}
