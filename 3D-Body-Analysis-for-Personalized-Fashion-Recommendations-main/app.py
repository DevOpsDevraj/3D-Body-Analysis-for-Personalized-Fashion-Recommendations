import streamlit as st
import os

from modules.pose_detection import detect_pose
from modules.body_analysis import analyze_body
from modules.body_classifier import classify_body
from modules.formal_recommender import recommend_formal_style
from modules.side_analysis import analyze_side_body

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="SmartFit", layout="wide")

# -------------------------
# SESSION STATE
# -------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

# -------------------------
# HOME PAGE
# -------------------------
if st.session_state.page == "home":

    st.title("SMARTFIT")
    st.subheader("AI-Based Styling System")

    st.markdown("""
    Analyze your body proportions and get personalized formal styling recommendations.
    """)

    if st.button("Start Analysis"):
        st.session_state.page = "upload"

# -------------------------
# UPLOAD PAGE
# -------------------------
elif st.session_state.page == "upload":

    st.header("Upload Your Images")

    st.markdown("""
    ### Instructions:
    • Full body should be visible (head to toe)  
    • Stand straight in natural posture  
    • Plain background (white preferred)  
    • Wear fitted or semi-fitted clothes  
    • Avoid angled or tilted photos  
    """)

    front_file = st.file_uploader("Upload Front Image", type=["jpg", "png"])
    side_file = st.file_uploader("Upload Side Image", type=["jpg", "png"])

    if st.button("Analyze"):

        if front_file and side_file:

            os.makedirs("temp", exist_ok=True)

            front_path = "temp/temp_front.jpg"
            side_path = "temp/temp_side.jpg"

            with open(front_path, "wb") as f:
                f.write(front_file.read())

            with open(side_path, "wb") as f:
                f.write(side_file.read())

            st.session_state.front = front_path
            st.session_state.side = side_path
            st.session_state.page = "result"

        else:
            st.error("Please upload both front and side images.")

# -------------------------
# RESULT PAGE
# -------------------------
elif st.session_state.page == "result":

    st.header("Analysis Result")

    front_kp, front_img = detect_pose(st.session_state.front)
    side_kp, side_img = detect_pose(st.session_state.side)

    front_analysis = analyze_body(front_kp)
    front_class = classify_body(front_analysis)

    side_analysis = analyze_side_body(side_kp)

    recommendations = recommend_formal_style(front_class, side_analysis)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(front_img, caption="Front View")

    with col2:
        st.image(side_img, caption="Side View")

    with col3:
        st.subheader("Body Analysis")

        st.write("Frame:", front_class["body_frame"])
        st.write("Proportion:", front_class["proportion"])
        st.write("Posture:", side_analysis["posture"])
        st.write("Belly:", side_analysis["belly"])
        st.write(side_analysis)

        st.subheader("Recommendations")

        for k, v in recommendations.items():
            st.write(f"{k}: {v}")

    if st.button("Analyze Another"):
        st.session_state.page = "home"