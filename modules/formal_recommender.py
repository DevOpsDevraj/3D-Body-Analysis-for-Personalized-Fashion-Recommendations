def recommend_formal_style(front_class, side_class):

    rec = {}

    # FRONT LOGIC
    if front_class["body_frame"] == "Broad Shoulders":
        rec["Blazer Fit"] = "Slim Fit"
        rec["Shoulder Padding"] = "Minimal"
    else:
        rec["Blazer Fit"] = "Regular Fit"
        rec["Shoulder Padding"] = "Standard"

    # SIDE LOGIC
    if side_class["belly"] == "Prominent":
        rec["Trouser Fit"] = "Mid Rise"
    else:
        rec["Trouser Fit"] = "Slim Tapered"

    if side_class["posture"] == "Leaning Forward":
        rec["Shoulder Padding"] = "Structured"

    rec["Jacket Length"] = "Standard"

    return rec

import cv2

def draw_body_proportions(image, keypoints):

    left_shoulder = keypoints.get(11)
    right_shoulder = keypoints.get(12)

    left_hip = keypoints.get(23)
    right_hip = keypoints.get(24)

    # Draw shoulder line
    cv2.line(image, left_shoulder, right_shoulder, (0,255,0), 3)

    # Draw hip line
    cv2.line(image, left_hip, right_hip, (255,0,0), 3)

    return image