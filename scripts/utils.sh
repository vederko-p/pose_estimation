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
    echo Download $file_name...
    gdown ${files_ids[i]}
    unzip "${files_names[i]}.zip" -d ${files_names[i]}
    rm "${files_names[i]}.zip"
  done

  cd -
}
