import math


def distance(p1, p2):
    if not p1 or not p2:
        return 0.0
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def midpoint(p1, p2):
    if not p1 or not p2:
        return None
    return ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)


def analyze_side_body(keypoints):
    results = {}

    left_shoulder = keypoints.get(11)
    right_shoulder = keypoints.get(12)
    left_hip = keypoints.get(23)
    right_hip = keypoints.get(24)
    left_knee = keypoints.get(25)
    right_knee = keypoints.get(26)
    left_ankle = keypoints.get(27)
    right_ankle = keypoints.get(28)
    left_wrist = keypoints.get(15)
    right_wrist = keypoints.get(16)

    shoulder_center = midpoint(left_shoulder, right_shoulder)
    hip_center = midpoint(left_hip, right_hip)
    knee_center = midpoint(left_knee, right_knee)
    ankle_center = midpoint(left_ankle, right_ankle)

    results["shoulder_hip_distance"] = distance(shoulder_center, hip_center)
    results["hip_ankle_distance"] = distance(hip_center, ankle_center)
    results["torso_ratio"] = round(
        distance(shoulder_center, hip_center) / max(distance(hip_center, ankle_center), 1.0),
        2
    )

    if shoulder_center and hip_center:
        results["shoulder_alignment"] = (
            "Aligned" if abs(shoulder_center[0] - hip_center[0]) < 20 else "Forward/Backward Shift"
        )
    else:
        results["shoulder_alignment"] = "Insufficient data"

    if knee_center and ankle_center:
        results["knee_to_ankle_distance"] = distance(knee_center, ankle_center)
    else:
        results["knee_to_ankle_distance"] = 0.0

    posture = "Good" if results["shoulder_alignment"] == "Aligned" and results["torso_ratio"] <= 1.2 else "Forward Lean"

    if results["torso_ratio"] < 0.95:
        belly = "Flat"
    elif results["torso_ratio"] <= 1.2:
        belly = "Moderate"
    else:
        belly = "Pronounced"

    if left_shoulder and right_shoulder and left_hip and right_hip:
        left_side = distance(left_shoulder, left_hip)
        right_side = distance(right_shoulder, right_hip)
        chest_balance = "Balanced" if abs(left_side - right_side) < 20 else "Unbalanced"
    else:
        chest_balance = "Insufficient data"

    if results["torso_ratio"] > 1.1:
        torso_type = "Long Torso"
    elif results["torso_ratio"] < 0.9:
        torso_type = "Short Torso"
    else:
        torso_type = "Balanced Torso"

    return {
        "posture": posture,
        "belly": belly,
        "chest_balance": chest_balance,
        "torso_type": torso_type,
        **results,
    }
