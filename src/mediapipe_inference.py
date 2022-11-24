import cv2
import mediapipe as mp


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

VIDEO_FILEPATH = '../data/first_test_data/1_workshop_1.mp4'


def main():
    v_cap = cv2.VideoCapture(VIDEO_FILEPATH)
    with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
        while v_cap.isOpened():
            success, image = v_cap.read()
            if not success:
                print('Empty video.')
                break

            # To improve performance, optionally mark the image as not
            # writeable to pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            # Draw the pose annotation on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            # Show results
            cv2.imshow('MediaPipe Pose', image)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

    v_cap.release()

if __name__ == '__main__':
    main()
