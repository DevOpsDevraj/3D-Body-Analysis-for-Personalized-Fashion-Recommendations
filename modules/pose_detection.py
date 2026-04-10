import cv2
import mediapipe as mp

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

pose = mp_pose.Pose(
    static_image_mode=True,
    model_complexity=2,
    enable_segmentation=False,
    min_detection_confidence=0.5
)


def detect_pose(image_path):
    
    # Read image
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(f"Image not found or invalid path: {image_path}"   )
    max_height = 800
    h, w = image.shape[:2]

    if h > max_height:
        scale = max_height / h
        image = cv2.resize(image, (int(w * scale), max_height))

    if image is None:
        raise ValueError("Image not found")

    # Convert to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Run pose detection
    results = pose.process(image_rgb)

    keypoints = {}

    if results.pose_landmarks:

        height, width, _ = image.shape

        for id, landmark in enumerate(results.pose_landmarks.landmark):

            x = int(landmark.x * width)
            y = int(landmark.y * height)

            keypoints[id] = (x, y)

        # Draw pose skeleton
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

    return keypoints, image

