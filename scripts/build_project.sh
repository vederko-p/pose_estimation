# Utils

check_and_mkdir() {
  local dirname=$1
  if [[ ! -d $dirname ]]
  then
    mkdir $dirname
  fi
}

# Install project requirements
echo Install project requirements...
pip -r requirements.txt

# Get yolo repository
echo 'Download yolov7-pose repository...'

MODELS_DIR="../src/models"
check_and_mkdir $MODELS_DIR

cd $MODELS_DIR
git clone --branch pose https://github.com/WongKinYiu/yolov7.git  # && cd yolov7

echo Install yolov7 requirements...
pip install -r requirements.txt
