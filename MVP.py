import cv2
import numpy as np
import time
from tensorflow.keras.models import load_model


IMG_SIZE = 300

try:
    model = load_model("./Yoga_Pose_Classification_Model.h5")
except Exception as e:
    print(f"Error loading model: {e}")
    print("Please ensure 'Yoga_Pose_Classification_Model.h5' is in the same directory as the script.")
    exit()


POSE_LABELS = ["downdog", "goddess","plank", "tree", "warrior2"]

POSE_FEEDBACK = {
    "downdog": "Nice Downward Dog! Press your heels toward the floor.",
    "goddess": "Powerful Goddess Pose! Try to sink your hips lower.",
    "plank": "Strong Plank! Keep your core tight and back straight.",
    "tree": "Beautiful Tree Pose! Focus on a single point to keep your balance.",
    "warrior2": "Fierce Warrior II! Extend your arms with energy."
}



def main():
    """
    Main function to run the real-time yoga pose detection.
    """
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) 

    last_detected_pose = None
    pose_start_time = None
    POSE_HOLD_DURATION = 3   # Seconds to hold a pose to trigger initial feedback.
    POSE_GOAL_DURATION = 10  # Seconds for the main timer goal for each pose.
    pose_timers = {pose: 0 for pose in POSE_LABELS} # Tracks cumulative time for each pose
    completed_poses = set() # Tracks poses that have met the 20-second goal
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Webcam opened successfully. Press 'q' to quit.")

    while True:
        # 1. Capture a frame from the webcam
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Create a copy of the frame to draw on
        output_frame = frame.copy()

        # 2. Pre-process the frame for the model
        # Resize the frame to the required input size (300x300)
        input_frame = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))
        
        # Convert frame from BGR (OpenCV's default) to RGB (model's expected format)
        input_frame = cv2.cvtColor(input_frame, cv2.COLOR_BGR2RGB)
        
        # Normalize pixel values to be between 0 and 1
        input_frame = input_frame.astype('float32') / 255.0
        
        # Expand the dimensions to create a batch of 1 (shape: 1, 300, 300, 3)
        input_frame = np.expand_dims(input_frame, axis=0)

        # 3. Make a prediction using the model
        predictions = model.predict(input_frame)
        
        # Get the index of the highest probability
        predicted_index = np.argmax(predictions[0])
        
        # Get the confidence score of the prediction
        confidence = np.max(predictions[0])
        
        # Get the corresponding pose label
        predicted_pose = POSE_LABELS[predicted_index]

        # 4. Display the prediction and confidence on the frame
        text = f"Pose: {predicted_pose}"
        # confidence_text = f"Confidence: {confidence:.2f}"
        
        # Set text properties
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.9
        color = (0, 255, 0)  # Green color
        thickness = 2

        # Put the text on the output frame
        cv2.putText(output_frame, text, (10, 30), font, font_scale, color, thickness, cv2.LINE_AA)
        # cv2.putText(output_frame, confidence_text, (10, 60), font, font_scale, color, thickness, cv2.LINE_AA)

        # --- Pose Hold and Timer Logic ---
        show_feedback = False # Initialize for each frame
        if predicted_pose == last_detected_pose:
            if pose_start_time is not None:
                # Update cumulative timer if the goal isn't met yet
                if predicted_pose not in completed_poses:
                    hold_time = time.time() - pose_start_time
                    pose_timers[predicted_pose] = hold_time

                # Check if initial feedback should be shown (after POSE_HOLD_DURATION)
                if pose_timers[predicted_pose] >= POSE_HOLD_DURATION:
                    show_feedback = True
        else:
            # If the pose has changed, reset the timer and update the last detected pose
            last_detected_pose = predicted_pose
            pose_start_time = time.time()
        # --- End of Pose Hold and Timer Logic ---

        # Display the current timer for the active pose
        if predicted_pose not in completed_poses:
            timer_text = f"Timer: {int(pose_timers.get(predicted_pose, 0))}/{POSE_GOAL_DURATION}s"
            cv2.putText(output_frame, timer_text, (10, 60), font, 0.7, (255, 255, 0), thickness)

        # Display pose-specific feedback if triggered
        if show_feedback:
            feedback_text = POSE_FEEDBACK.get(predicted_pose, "Great job holding the pose!")
            cv2.putText(output_frame, feedback_text, (10, 90), font, 0.7, (0, 165, 255), thickness, cv2.LINE_AA)
        
        # Check for goal completion and display messages
        if pose_timers.get(predicted_pose, 0) >= POSE_GOAL_DURATION and predicted_pose not in completed_poses:
            completed_poses.add(predicted_pose)
            cv2.putText(output_frame, "Well Done!", (150, 150), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 255, 255), 3)

        # 5. Show the final frame to the user
        cv2.imshow('Real-time Yoga Pose Detection', output_frame)

        # 6. Check for user input to quit
        # The loop breaks when the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 7. Clean up resources
    print("Exiting application...")
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()