# Pose Estimation


# Инструкция установки и запуска

## Установка

Склонировать репозиторий:

```
git clone https://github.com/vederko-p/pose_estimation.git && cd pose_estimation
```

Установить зависимости, скачать тестовые данные и веса моделей:

```
cd scripts
bash build_project.sh
```

## Запуск

Перед запуском любой модели необходимо убедиться, что пути к ключевым файлам указаны верно.

### Mediapipe

Запуск:

```
cd scr
python3 mediapipe_inference.py
```

Путь к видеофайлу указан в константе `VIDEO_FILEPATH`. По умолчанию указан файл `1_workshop_1.mp4`.

### Yolov7-Pose

Запуск:

```
cd scripts
bash yolo_pose_detect.sh
```

Путь к видеофайлу указан в константе `FILEPATH`. По умолчанию указан файл `1_workshop_1.mp4`.

### MMPose + MMDet

Запуск:

```
cd scr
python3 mmpose_inference.py
```

Путь к видеофайлу указан в константе `VIDEO_PATH`. По умолчанию указан файл `1_workshop_1.mp4`.

### MMPose + Yolov7

Запуск:

```
cd src
python3 mmpose_yolov7_inference.py
```

Путь к видеофайлу указан в константе `VIDEO_PATH`. По умолчанию указан файл `1_workshop_1.mp4`.

