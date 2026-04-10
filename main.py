from modules.pose_detection import detect_pose
from modules.body_analysis import analyze_body
from modules.body_classifier import classify_body
from modules.formal_recommender import recommend_formal_style
from modules.side_analysis import analyze_side_body
from utils.input_handler import load_image_path

import cv2
import numpy as np
import os


def resize_images(front, side, target_height=600):

    h1, w1 = front.shape[:2]
    h2, w2 = side.shape[:2]

    scale1 = target_height / h1
    scale2 = target_height / h2

    front = cv2.resize(front, (int(w1 * scale1), target_height))
    side = cv2.resize(side, (int(w2 * scale2), target_height))

    return front, side


def run():
    base_dir = os.path.dirname(__file__)

    front_image_path = load_image_path(base_dir, os.path.join("assets", "front_sample.jpg"))
    side_image_path = load_image_path(base_dir, os.path.join("assets", "side_sample.jpg"))

    front_keypoints, front_image = detect_pose(front_image_path)
    front_analysis = analyze_body(front_keypoints)
    classification = classify_body(front_analysis)

    side_keypoints, side_image = detect_pose(side_image_path)
    side_analysis = analyze_side_body(side_keypoints)

    front_image, side_image = resize_images(front_image, side_image)

    combined = cv2.hconcat([front_image, side_image])
    recommendations = recommend_formal_style(classification)

    print("\nSMARTFIT RESULT\n")
    for r in recommendations:
        print("-", r)

    print("\nSIDE IMAGE ANALYSIS\n")
    for name, value in side_analysis.items():
        print(f"- {name.replace('_', ' ').title()}: {value}")

    panel_width = 500
    panel = np.zeros((combined.shape[0], panel_width, 3), dtype=np.uint8)

    cv2.putText(panel,
                "SMARTFIT RESULT",
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (240, 240, 255),
                2)

    y = 120
    for r in recommendations:
        cv2.putText(panel,
                    "-> " + r,
                    (20, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (240, 240, 255),
                    2)
        y += 50

    final_view = cv2.hconcat([combined, panel])
    cv2.imshow("SmartFit Analysis", final_view)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run()
