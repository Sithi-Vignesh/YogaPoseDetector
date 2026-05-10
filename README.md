# 🧘‍♂️ Yoga Pose Detector

A real-time AI-powered yoga pose detection and classification system built with Python, OpenCV, TensorFlow, and Streamlit. The app detects your yoga pose via webcam, gives live feedback, tracks your hold time, and includes an AI yoga assistant chatbot.

---

## ✨ Features

- **Real-time pose detection** — detects yoga poses live via webcam using a trained CNN model
- **5 yoga poses supported** — Downward Dog, Goddess, Plank, Tree, Warrior II
- **Live feedback** — personalized coaching tips displayed on screen for each pose
- **Gamified hold timer** — tracks how long you hold each pose with a 10-second goal
- **Pose guide carousel** — step-by-step instructions and images for each pose
- **AI yoga chatbot** — built-in Gemini-powered assistant to answer yoga questions

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Pose Detection Model | TensorFlow / Keras (CNN) |
| Computer Vision | OpenCV |
| Web Interface | Streamlit |
| AI Chatbot | Google Gemini API |
| Language | Python |

---

## 📁 Project Structure

```
YogaPoseDetector/
├── MVP.py              # Core real-time webcam pose detection (OpenCV)
├── GS.py               # Streamlit UI — pose guide + launcher + chatbot
├── launcher.py         # App launcher script
├── sample.py           # Sample/testing script
├── requirements.txt    # Python dependencies
└── .gitignore
```

> ⚠️ The trained model file (`Yoga_Pose_Classification_Model.h5`) is not included in this repo due to file size (~368MB).
> Download it here: https://drive.google.com/file/d/1y0anmTJgJi_O9ex-SpHDhabmVWqAGGej/view?usp=sharing

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Sithi-Vignesh/YogaPoseDetector.git
cd YogaPoseDetector
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Download the model
Download `Yoga_Pose_Classification_Model.h5` from the link above and place it in the root directory.

### 4. Add your Gemini API key
Create a `.streamlit/secrets.toml` file:
```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

### 5. Run the app
```bash
streamlit run GS.py
```

Then click **"Start Pose Detector"** to launch the real-time webcam window.

---

## 🧘 Supported Poses

| Pose | Hold Goal |
|---|---|
| Downward Dog | 10 seconds |
| Goddess | 10 seconds |
| Plank | 10 seconds |
| Tree | 10 seconds |
| Warrior II | 10 seconds |

---

## 📸 How It Works

1. Webcam captures live video frames
2. Each frame is resized to 300×300 and normalized
3. The CNN model predicts the yoga pose with a confidence score
4. If you hold the pose for 3+ seconds, personalized feedback appears
5. Holding for 10 seconds marks the pose as completed 🎉

---

## 🔮 Future Improvements

- Add more yoga poses
- Show confidence score on screen
- Add skeleton/keypoint overlay using MediaPipe
- Mobile-friendly version
- Pose history and session summary

---

## 👨‍💻 Author

**Sithi Vignesh** — CS (AI/ML), VIT Vellore
[GitHub](https://github.com/Sithi-Vignesh) | [LinkedIn](https://linkedin.com/in/sithi-vignesh)
