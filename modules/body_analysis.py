import math


def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)


def analyze_body(keypoints):

    results = {}

    # IMPORTANT LANDMARKS
    nose = keypoints.get(0)

    left_shoulder = keypoints.get(11)
    right_shoulder = keypoints.get(12)

    left_elbow = keypoints.get(13)
    right_elbow = keypoints.get(14)

    left_wrist = keypoints.get(15)
    right_wrist = keypoints.get(16)

    left_hip = keypoints.get(23)
    right_hip = keypoints.get(24)

    left_ankle = keypoints.get(27)
    right_ankle = keypoints.get(28)

    # Shoulder width
    shoulder_width = distance(left_shoulder, right_shoulder)

    # Hip width
    hip_width = distance(left_hip, right_hip)

    # Waist approximation (midpoint between shoulders & hips)
    waist_width = shoulder_width * 0.75

    # Torso length
    torso_length = distance(left_shoulder, left_hip)

    # Leg length
    leg_length = distance(left_hip, left_ankle)

    # Arm length
    arm_length = distance(left_shoulder, left_wrist)

    # Body height
    body_height = distance(nose, left_ankle)

    # Face height approximation
    face_height = body_height * 0.13

    # Ratios
    shoulder_hip_ratio = shoulder_width / hip_width
    torso_leg_ratio = torso_length / leg_length
    face_body_ratio = body_height / face_height

    results["shoulder_width"] = shoulder_width
    results["waist_width"] = waist_width
    results["hip_width"] = hip_width

    results["shoulder_hip_ratio"] = shoulder_hip_ratio
    results["torso_leg_ratio"] = torso_leg_ratio
    results["face_body_ratio"] = face_body_ratio

    results["arm_length"] = arm_length

    return results

import cv2

def draw_body_proportions(image, keypoints):

    import cv2

    left_shoulder = keypoints.get(11)
    right_shoulder = keypoints.get(12)

    left_hip = keypoints.get(23)
    right_hip = keypoints.get(24)

    left_knee = keypoints.get(25)
    right_knee = keypoints.get(26)

    left_hip_adj, right_hip_adj = estimate_hip_width(image, left_hip, right_hip)

    if left_shoulder and right_shoulder:

        cv2.line(image, left_shoulder, right_shoulder, (0,255,0), 3)

        mid_x = int((left_shoulder[0] + right_shoulder[0]) / 2)
        mid_y = int((left_shoulder[1] + right_shoulder[1]) / 2)

        cv2.putText(image,
                    "Shoulder Width",
                    (mid_x - 80, mid_y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0,255,0),
                    2)

    if left_hip and right_hip:

        cv2.line(image, left_hip_adj, right_hip_adj, (255,0,0), 3)

        mid_x = int((left_hip[0] + right_hip[0]) / 2)
        mid_y = int((left_hip[1] + right_hip[1]) / 2)

        cv2.putText(image,
                    "Hip Width",
                    (mid_x - 60, mid_y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255,0,0),
                    2)

    return image

def estimate_hip_width(image, left_hip, right_hip):

    import numpy as np

    height, width = image.shape[:2]

    # compute hip scan line
    y = int((left_hip[1] + right_hip[1]) / 2) - 20

    # keep y inside image
    y = max(0, min(y, height - 1))

    # keep x values inside image
    left_x = max(0, min(left_hip[0], width - 1))
    right_x = max(0, min(right_hip[0], width - 1))

    # scan left
    left_edge = left_x
    for x in range(left_x, -1, -1):
        if np.mean(image[y, x]) > 240:   # detect background
            break
        left_edge = x

    # scan right
    right_edge = right_x
    for x in range(right_x, width):
        if np.mean(image[y, x]) > 240:
            break
        right_edge = x

    return (left_edge, y), (right_edge, y)