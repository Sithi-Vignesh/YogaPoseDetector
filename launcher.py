import streamlit as st
import subprocess
import psutil
import sys

st.set_page_config(page_title="Yoga Pose Detector", page_icon="🧘‍♂️")

st.title("🧘‍♂️ Yoga Pose Detector")
st.info("Use the launcher below to start the real-time detection window, or browse the pose guide to practice.")

# --- Session State Management ---
if "mvp_process" not in st.session_state:
    st.session_state.mvp_process = None

def find_process_by_pid(pid):
    """Check if a process with the given PID is still running."""
    return psutil.pid_exists(pid)

# --- Pose Carousel Guide ---
st.header("📖 Yoga Pose Guide")

POSE_GUIDE = [
    {
        "name": "Downward Dog",
        "image": "https://images.squarespace-cdn.com/content/v1/55a9457de4b0e82a7749b6d3/1600771298735-Q6NP7GFVZBT6TMQV2GC6/YOGARU_Adho+Mukha+Svanasana_PB.png?format=1000w",
        "steps": [
            "1. Start on your hands and knees in a tabletop position.",
            "2. Tuck your toes and lift your hips up and back, forming an inverted 'V' shape.",
            "3. Press firmly into your hands, spread your fingers, and let your head hang freely."
        ]
    },
    {
        "name": "Goddess",
        "image": "https://images.squarespace-cdn.com/content/v1/55a9457de4b0e82a7749b6d3/1600084062623-PYLH6TRKP9E8UH2P49HI/image-asset.png",
        "steps": [
            "1. Stand with your feet wide apart, with toes pointing outwards.",
            "2. Bend your knees and lower your hips into a squat, keeping thighs parallel to the floor.",
            "3. Raise your arms to shoulder height and bend elbows at 90 degrees, palms facing forward."
        ]
    },
    {
        "name": "Tree",
        "image": "https://images.squarespace-cdn.com/content/v1/55a9457de4b0e82a7749b6d3/1600084022256-JK85LKMG6SC1ZQ5991A7/YOGARU_Vrksasana_PB.png?format=1000w",
        "steps": [
            "1. Start in Mountain Pose. Shift your weight to your left foot.",
            "2. Place the sole of your right foot on your inner left thigh or calf (avoid the knee).",
            "3. Bring your hands to your heart in a prayer position and find your balance."
        ]
    },
    {
        "name": "Plank",
        "image": "https://tse3.mm.bing.net/th/id/OIP.UAESkA6gvipt_3KZpD_-BwHaEt?w=1500&h=955&rs=1&pid=ImgDetMain&o=7&rm=3",
        "steps": [
            "1. Start in a push-up position with your hands directly under your shoulders.",
            "2. Engage your core and glutes to form a straight line from your head to your heels.",
            "3. Hold the position, breathing steadily. Avoid letting your hips sag or rise."
        ]
    },
    {
        "name": "Warrior II",
        "image": "https://tse4.mm.bing.net/th/id/OIP.efstqdHH6i8kzSAa1JpiFQAAAA?rs=1&pid=ImgDetMain&o=7&rm=3",
        "steps": [
            "1. Stand with feet wide. Turn your right foot out 90 degrees and your left foot in slightly.",
            "2. Raise your arms parallel to the floor, reaching out actively to your sides.",
            "3. Bend your right knee over your right ankle and gaze over your right fingertips."
        ]
    }
]

if "pose_index" not in st.session_state:
    st.session_state.pose_index = 0

current_pose = POSE_GUIDE[st.session_state.pose_index]

col1, col2 = st.columns([1, 4])

with col1:
    if st.button("⬅️ Prev", use_container_width=True):
        st.session_state.pose_index = (st.session_state.pose_index - 1) % len(POSE_GUIDE)
        st.rerun()
    if st.button("Next ➡️", use_container_width=True):
        st.session_state.pose_index = (st.session_state.pose_index + 1) % len(POSE_GUIDE)
        st.rerun()

with col2:
    with st.container(border=True):
        st.subheader(current_pose["name"])
        st.image(current_pose["image"])
        for step in current_pose["steps"]:
            st.markdown(f"- {step}")

st.markdown("---")

# --- MVP Launcher ---
with st.expander("🚀 Launch Real-Time Detector", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Start Pose Detector", use_container_width=True):
            if st.session_state.mvp_process and find_process_by_pid(st.session_state.mvp_process.pid):
                st.warning("Detector is already running.")
            else:
                st.info("Starting `MVP.py`... A new window will open.")
                process = subprocess.Popen(
                    [sys.executable, "MVP.py"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True
                )
                st.session_state.mvp_process = process
                st.rerun()

    with col2:
        if st.button("⏹️ Stop Pose Detector", use_container_width=True):
            if st.session_state.mvp_process and find_process_by_pid(st.session_state.mvp_process.pid):
                pid = st.session_state.mvp_process.pid
                st.info(f"Stopping process {pid}...")
                try:
                    parent = psutil.Process(pid)
                    for child in parent.children(recursive=True):
                        child.terminate()
                    parent.terminate()
                    st.session_state.mvp_process = None
                    st.success("Detector stopped.")
                except psutil.NoSuchProcess:
                    st.warning("Process was already closed.")
                    st.session_state.mvp_process = None
                st.rerun()
            else:
                st.warning("Detector is not running.")

st.markdown("---")

# --- Script Output Log (for debugging) ---
st.subheader("🕵️‍♂️ Script Output Log")
st.info("If the video window doesn't appear, any errors from the script will be shown below.")

if st.session_state.mvp_process:
    # Read and display the output from the script
    output = st.session_state.mvp_process.stdout.read()
    st.code(output, language="log")