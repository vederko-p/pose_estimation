. utils.sh


# Install project requirements
echo Install project requirements...
pip install -r "../requirements.txt"


# Set models directory
echo 'Check model directory...'
MODELS_DIR="../src/models"
check_and_mkdir $MODELS_DIR
cd $MODELS_DIR


YOLOV7_REPOSIROTY_LINK="https://github.com/WongKinYiu/yolov7.git"

# Get yolov7 detector
echo 'Download yolov7-detector repository...'
YV7D_directory="yolov7_detector"
check_and_mkdir $YV7D_directory
git clone $YOLOV7_REPOSIROTY_LINK $YV7D_directory
install_requirements $YV7D_directory

# Get yolov7 pose
YV7P_directory="yolov7_pose"
check_and_mkdir $YV7P_directory
git clone --branch pose  $YOLOV7_REPOSIROTY_LINK $YV7P_directory
install_requirements $YV7P_directory


# Get MMPose
mmpose_directory="mmpose"
echo 'Download mmpose'
pip install openmim
mim install mmcv-full
git clone https://github.com/open-mmlab/mmpose.git && cd $mmpose_directory
pip install -e .

# Get MMDet as module
pip install mmdet
