
import sys
sys.path.append('models/yolov7_detector')

import os
from typing import Union, Tuple

import cv2
import mmcv
import numpy as np
import torch

from mmpose.apis import (inference_top_down_pose_model, init_pose_model,
                         vis_pose_result)

try:
    from mmdet.apis import inference_detector, init_detector
    has_mmdet = True
except (ImportError, ModuleNotFoundError):
    has_mmdet = False

from models.experimental import attempt_load
from utils.general import check_img_size, non_max_suppression, scale_coords
from utils.torch_utils import TracedModel, time_synchronized
from utils.datasets import letterbox


MMPOSE_CONFIG = 'models/mmpose/configs/body/2d_kpt_sview_rgb_img/topdown_heatmap/coco/hrnet_w48_coco_256x192.py'
MMPOSE_CHECKPOINT = 'https://download.openmmlab.com/mmpose/top_down/hrnet/hrnet_w48_coco_256x192-b9e0b3ab_20200708.pth'

YOLO_WEIGHTS_PATH = 'weights/yolov7_detector/yolov7.pt'
IMG_SIZE = 640
STRIDE = 32

DEVICE = 'cuda:0'


VIDEO_PATH = '../data/first_test_data/1_workshop_1.mp4'
SHOW = True
OUT_VIDEO_ROOT = '../data'
SAVE_OUT_VIDEO = True

IMG_SIZE_H = 1920
IMG_SIZE_W = 1080


def init_yolo_model():
    model = attempt_load(YOLO_WEIGHTS_PATH, map_location=DEVICE)
    stride = int(model.stride.max())
    imgsz = check_img_size(IMG_SIZE, s=stride)
    model = TracedModel(model, DEVICE, imgsz)
    return model


def prep_yolo_img(img0, img_size, stride):
    img = letterbox(img0, img_size, stride=stride)[0]
    img = img[:, :, ::-1].transpose(2, 0, 1)
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).to(DEVICE)
    img = img.float()
    img /= 255.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)
    return img


def convert_annot_xywh2xyxy(
        bx: float, by: float, bw: float, bh: float,
        img_w: Union[float, int], img_h: Union[float, int]
) -> Tuple[int, int, int, int]:
    """Convert yolo-like box annotation into
    top-left bottom-right box annotation.

    Parameters
    ----------
    bx: float
        Box x center.
    by: float
        Box y center.
    bw: float
        Box width.
    bh: float
        Box height.
    img_w: Union[float, int]
        Image width.
    img_h: Union[float, int]
        Image height.

    Returns
    -------
    left_x : int
        Box left x.
    top_y : int
        Box top y.
    right_x : int
        Box right x.
    botom_y : int
        Box bottom y."""
    left_x = int((bx - bw / 2) * img_w)
    top_y = int((by - bh / 2) * img_h)
    right_x = int((bx + bw / 2) * img_w)
    botom_y = int((by + bh / 2) * img_h)
    return left_x, top_y, right_x, botom_y


def main():
    # yolov7 detecor
    yolo_det = init_yolo_model()
    conf_thres = 0.25
    iou_thres = 0.45
    # classes = [0]  # only person
    classes = None
    agnostic_nms = False
    half = False

    # mmpose
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
    return_heatmap = False
    output_layer_names = None
    radius = 4
    thickness = 1
    kpt_thr = 0.3
    person_class = 0
    total_ms = 0
    for frame_id, cur_frame in enumerate(mmcv.track_iter_progress(video)):
        t0 = time_synchronized()
        # keep the person class bounding boxes.
        img = prep_yolo_img(cur_frame, IMG_SIZE, STRIDE)
        with torch.no_grad():
            pred = yolo_det(img, augment=False)[0]
        pred = non_max_suppression(
            pred, conf_thres, iou_thres, classes=classes, agnostic=agnostic_nms
        )[0]
        pred[:, :4] = scale_coords(
            img.shape[2:], pred[:, :4], cur_frame.shape).round()
        person_results = [
            {'bbox': d[:4].cpu().numpy()} for d in pred
            if int(d[5]) == person_class
        ]

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
        ms = round(t1 - t0, 3)
        total_ms += ms
        mean_ms = round(total_ms / (frame_id+1), 3)
        print(f' | current: {ms} s | mean: {mean_ms} s')

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
