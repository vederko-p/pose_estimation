YOLO_DIR="../src/models/yolov7_pose"
WEIGHTS_PATH="../src/weights/yolov7_pose_estimation/yolov7-w6-pose.pt"

FILEPATH="../data/first_test_data/1_workshop_1.mp4"

cd $YOLO_DIR

python3 detect.py --weights $WEIGHTS_PATH --source $FILEPATH --view-img --kpt-label
