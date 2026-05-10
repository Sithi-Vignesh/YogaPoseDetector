import streamlit as st
import subprocess
import psutil
import sys
import google.generativeai as genai

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
    # Check if the process is still running.
    is_running = find_process_by_pid(st.session_state.mvp_process.pid)
    
    # poll() returns None if the process is still running, otherwise it returns the exit code.
    return_code = st.session_state.mvp_process.poll()

    if return_code is not None:
        # The process has terminated. Read all output it produced.
        # This is useful for capturing startup errors.
        output = st.session_state.mvp_process.stdout.read()
        st.code(output, language="log")
    else:
        st.success("✅ The pose detector process is running.")

st.markdown("---")

# --- Gemini Chatbot ---

# Custom CSS for the floating chatbot
st.markdown("""
<style>
    #chat-container {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 1000;
    }
    .chat-window {
        height: 500px;
        width: 400px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        display: flex;
        flex-direction: column;
        overflow: hidden;
        background-color: #f9f9f9;
    }
    .chat-header {
        background-color: #0d6efd;
        color: white;
        padding: 10px;
        text-align: center;
        font-weight: bold;
    }
    .chat-history {
        flex-grow: 1;
        overflow-y: auto;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

def initialize_gemini():
    """Initializes the Gemini model with the hardcoded API key."""
    try:
        # Securely access the API key from Streamlit's secrets
        if "GEMINI_API_KEY" not in st.secrets:
            st.error("Gemini API key not found. Please add it to your .streamlit/secrets.toml file.")
            return None
        
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-pro')
        # Start a chat with a system instruction
        chat = model.start_chat(history=[
            {
                "role": "user",
                "parts": ["You are a friendly and knowledgeable yoga assistant. Your goal is to help users with their yoga practice by answering questions about poses, benefits, and techniques. Keep your answers concise and encouraging."]
            },
            {
                "role": "model",
                "parts": ["Namaste! I am your personal yoga assistant. How can I help you with your practice today?"]
            }
        ])
        return chat
    except Exception as e:
        st.error(f"Failed to initialize Gemini: {e}")
        return None

# Initialize chat in session state
if "gemini_chat" not in st.session_state:
    st.session_state.gemini_chat = None

if not st.session_state.gemini_chat:
    st.session_state.gemini_chat = initialize_gemini()

# Create a container for the chatbot UI
with st.container():
    # Use an expander to create a "floating" chat window effect
    with st.expander("💬 Chat with Yoga AI", expanded=True):
        if not st.session_state.gemini_chat:
            st.warning("Chatbot could not be initialized. Please check your API key in secrets.toml.")
        else:
            # Display chat history
            for message in st.session_state.gemini_chat.history:
                # The first message is a system instruction, so we skip it
                if message.role == "user" and "You are a friendly" in message.parts[0].text:
                    continue
                role = "assistant" if message.role == "model" else message.role
                with st.chat_message(role):
                    st.markdown(message.parts[0].text)

            # Chat input for the user
            if prompt := st.chat_input("Ask about a yoga pose..."):
                # Add user message to chat history
                with st.chat_message("user"):
                    st.markdown(prompt)

                # Get response from Gemini
                try:
                    with st.spinner("Thinking..."):
                        response = st.session_state.gemini_chat.send_message(prompt)
                    with st.chat_message("assistant"):
                        st.markdown(response.text)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                
                # Rerun to display the latest messages
                st.rerun()