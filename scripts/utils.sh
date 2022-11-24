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
