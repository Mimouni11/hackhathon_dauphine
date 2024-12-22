import cv2
import mediapipe as mp
import json
import numpy as np

# Initialize MediaPipe modules
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Initialize a dictionary to store keypoints data
keypoints_data = []

# Function to normalize keypoints
def normalize_keypoints(keypoints, width, height):
    """
    Normalize keypoints to the range [0, 1] for x and y coordinates, and scale z values.
    """
    normalized = []
    for x, y, z in keypoints:
        normalized.append([
            x * width,            # Scale x to pixel space
            (1 - y) * height,     # Scale and invert y for pixel space
            z                     # Keep z as-is or scale if needed
        ])
    return normalized

# Function to smooth keypoints using a moving average
def smooth_keypoints(keypoints_list, window_size=3):
    """
    Apply a moving average to smooth the keypoints over time.
    Handles lists of lists (e.g., multiple hands).
    """
    smoothed = []
    for i in range(len(keypoints_list)):
        # Smooth each set of keypoints independently
        frame_smoothed = []
        for hand_index in range(len(keypoints_list[i])):
            window = [
                keypoints_list[j][hand_index]
                for j in range(max(0, i - window_size + 1), i + 1)
                if hand_index < len(keypoints_list[j])  # Ensure the index exists
            ]
            frame_smoothed.append(np.mean(window, axis=0).tolist())
        smoothed.append(frame_smoothed)
    return smoothed

# Visualize keypoints on the video and save keypoints data to a JSON file
def visualize_keypoints_and_save(video_path, output_path, json_output_path):
    cap = cv2.VideoCapture(video_path)
    out = None
    pose = mp_pose.Pose()
    hands = mp_hands.Hands()

    # Get video dimensions
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Temporary storage for smoothing
    pose_frames = []
    hand_frames = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pose_results = pose.process(frame_rgb)
        hand_results = hands.process(frame_rgb)

        # Initialize the frame data for keypoints
        frame_data = {"pose": [], "hands": []}

        # Draw pose landmarks and store pose keypoints
        if pose_results.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            pose_landmarks = [[l.x, l.y, l.z] for l in pose_results.pose_landmarks.landmark]
            # Normalize and append to temporary storage
            pose_frames.append(normalize_keypoints(pose_landmarks, width, height))

        # Draw hand landmarks and store hand keypoints
        if hand_results.multi_hand_landmarks:
            hands_data = []
            for hand_landmarks in hand_results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                hand_landmarks_data = [[l.x, l.y, l.z] for l in hand_landmarks.landmark]
                # Normalize and append
                hands_data.append(normalize_keypoints(hand_landmarks_data, width, height))
            hand_frames.append(hands_data)

        # Add the smoothed data to frame_data
        if len(pose_frames) > 0:
            frame_data["pose"] = smooth_keypoints([pose_frames], window_size=3)[-1]
        if len(hand_frames) > 0:
            frame_data["hands"] = smooth_keypoints(hand_frames, window_size=3)[-1]

        # Add frame data to the keypoints list
        keypoints_data.append(frame_data)

        # Initialize video writer
        if out is None:
            height, width, _ = frame.shape
            out = cv2.VideoWriter(
                output_path, cv2.VideoWriter_fourcc(*'mp4v'), 30, (width, height))

        out.write(frame)
        # cv2.imshow("Keypoints Visualization", frame)

        # Break on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()

    # Save the keypoints data to a JSON file
    with open(json_output_path, 'w') as json_file:
        json.dump(keypoints_data, json_file, indent=4)  # Save as formatted JSON

    cv2.destroyAllWindows()

# Example usage
visualize_keypoints_and_save("output_translation.mp4", "output_visualization.mp4", "keypoints_data.json")
