
import os

import cv2
import mmcv
import numpy as np

from mmpose.apis import (inference_top_down_pose_model, init_pose_model,
                         vis_pose_result, process_mmdet_results)

try:
    from mmdet.apis import inference_detector, init_detector
    has_mmdet = True
except (ImportError, ModuleNotFoundError):
    has_mmdet = False

import sys
sys.path.append('models/yolov7_detector')
from utils.torch_utils import time_synchronized


MMDET_CONFIG = 'models/mmpose/demo/mmdetection_cfg/faster_rcnn_r50_fpn_coco.py'
MMDET_CHECKPOINT = 'https://download.openmmlab.com/mmdetection/v2.0/faster_rcnn/faster_rcnn_r50_fpn_1x_coco/faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth'

MMPOSE_CONFIG = 'models/mmpose/configs/body/2d_kpt_sview_rgb_img/topdown_heatmap/coco/hrnet_w48_coco_256x192.py'
MMPOSE_CHECKPOINT = 'https://download.openmmlab.com/mmpose/top_down/hrnet/hrnet_w48_coco_256x192-b9e0b3ab_20200708.pth'

DEVICE = 'cuda:0'


# VIDEO_PATH = '../data/first_test_data/3_assasins_short.mp4'
VIDEO_PATH = '../data/first_test_data/1_workshop_1.mp4'
SHOW = True
OUT_VIDEO_ROOT = '../data'
SAVE_OUT_VIDEO = True


def main():
    # Model
    det_model = init_detector(
        MMDET_CONFIG, MMDET_CHECKPOINT, device=DEVICE)

    pose_model = init_pose_model(
        MMPOSE_CONFIG, MMPOSE_CHECKPOINT, device=DEVICE)

    # Video
    video = mmcv.VideoReader(VIDEO_PATH)
    assert video.opened, f'Failed to load video file {VIDEO_PATH}'

    fps = video.fps
    size = (video.width, video.height)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    videoWriter = cv2.VideoWriter(
        os.path.join(OUT_VIDEO_ROOT, f'vis_{os.path.basename(VIDEO_PATH)}'),
        fourcc, fps, size)

    # Inference
    det_cat_id = 1
    return_heatmap = False
    output_layer_names = None
    radius = 4
    thickness = 1
    kpt_thr = 0.3
    total_s = 0
    for frame_id, cur_frame in enumerate(mmcv.track_iter_progress(video)):
        t0 = time_synchronized()
        # keep the person class bounding boxes.
        mmdet_results = inference_detector(det_model, cur_frame)
        person_results = process_mmdet_results(mmdet_results, det_cat_id)

        # test a single image, with a list of bboxes.
        pose_results, returned_outputs = inference_top_down_pose_model(
            pose_model,
            cur_frame,
            person_results,
            format='xyxy',
            dataset=None,
            dataset_info=None,
            return_heatmap=return_heatmap,
            outputs=output_layer_names)

        t1 = time_synchronized()
        s = round(t1 - t0, 3)
        total_s += s
        mean_s = round(total_s / (frame_id + 1), 3)
        print(f' | current: {s} s | mean: {mean_s} s')

        # show the results
        vis_frame = vis_pose_result(
            pose_model,
            cur_frame,
            pose_results,
            radius=radius,
            thickness=thickness,
            dataset=None,
            dataset_info=None,
            kpt_score_thr=kpt_thr,
            show=False)

        if SHOW:
            cv2.imshow('Frame', vis_frame)

        if SAVE_OUT_VIDEO:
            videoWriter.write(vis_frame)

        if SHOW and cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if SAVE_OUT_VIDEO:
        videoWriter.release()
    if SHOW:
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
