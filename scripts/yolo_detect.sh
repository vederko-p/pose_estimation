YOLO_DIR="../src/models/yolov7"
WEIGHTS_PATH="/home/maksim/Desktop/Projects/neft_project/pose_estimation/src/models/weights/yolov7-w6-person.pt"

FILEPATH="/home/maksim/Desktop/Projects/neft_project/pose_estimation/data/2_football.jpg"

cd $YOLO_DIR

python3 detect.py --weights $WEIGHTS_PATH --source $FILEPATH --view-img
