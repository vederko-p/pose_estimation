YOLO_DIR="../src/models/yolov7_detector"
WEIGHTS_PATH="/home/skibinmv/Desktop/neft_project/pose_estimation/src/weights/yolov7_detector/yolov7.pt"

FILEPATH="/home/skibinmv/Desktop/neft_project/pose_estimation/data/first_test_data/1_workshop_1.mp4"

cd $YOLO_DIR

python3 detect.py --weights $WEIGHTS_PATH --source $FILEPATH --view-img
