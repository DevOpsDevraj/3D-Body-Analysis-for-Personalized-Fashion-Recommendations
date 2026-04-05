def classify_body(analysis):

    classification = {}

    shoulder_hip_ratio = analysis["shoulder_hip_ratio"]
    torso_leg_ratio = analysis["torso_leg_ratio"]
    face_body_ratio = analysis["face_body_ratio"]

    # Shoulder structure
    if shoulder_hip_ratio > 1.1:
        classification["body_frame"] = "Broad Shoulders"
    elif shoulder_hip_ratio < 0.9:
        classification["body_frame"] = "Hip Dominant"
    else:
        classification["body_frame"] = "Balanced Frame"

    # Torso vs legs
    if torso_leg_ratio > 1:
        classification["proportion"] = "Long Torso"
    elif torso_leg_ratio < 0.75:
        classification["proportion"] = "Long Legs"
    else:
        classification["proportion"] = "Balanced Proportion"

    # Face-body proportion
    if face_body_ratio >= 7:
        classification["aesthetic_ratio"] = "Ideal Proportion"
    else:
        classification["aesthetic_ratio"] = "Compact Proportion"

    return classification