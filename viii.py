import os
import json
import cv2
import numpy as np

# Load the WLASL dataset
def load_dataset(json_path):
    with open(json_path, 'r') as file:
        dataset = json.load(file)
    return dataset

# Map a word to its corresponding video
def map_word_to_video(word, dataset, video_dir="videos"):
    for entry in dataset:
        if entry['gloss'].lower() == word.lower():  # Case-insensitive match
            for instance in entry['instances']:
                video_id = instance['video_id']
                video_path = f"{video_dir}/{video_id}.mp4"
                if os.path.exists(video_path):  # Check if the video exists
                    return video_path
            print(f"No available video found for word '{word}', but instances exist.")
            return None
    print(f"Word '{word}' not found in dataset.")
    return None

# Translate input text to a sequence of video paths
def translate_text_to_videos(text_file, dataset, video_dir="videos"):
    with open(text_file, 'r', encoding="utf-8") as file:
        text = file.read().strip().split()
    
    video_paths = []
    for word in text:
        video_path = map_word_to_video(word, dataset, video_dir)
        if video_path:
            video_paths.append(video_path)
        else:
            print(f"Word '{word}' not found in dataset.")
    return video_paths

# Combine videos into a single sequence using OpenCV
def create_sign_language_video(video_paths, output_path="output_translation.mp4"):
    try:
        frames = []
        for video_path in video_paths:
            cap = cv2.VideoCapture(video_path)
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frames.append(frame)
            cap.release()

        # Write all frames to the output video file
        if frames:
            height, width, layers = frames[0].shape
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, 25, (width, height))
            for frame in frames:
                out.write(frame)
            out.release()
            return output_path
        else:
            print("No frames to save.")
            return None
    except Exception as e:
        print(f"Error creating video: {e}")
        return None

# Main function
def main():
    # Paths to required files and directories
    dataset_json_path = "WLASL_v0.3.json"  # Path to the WLASL dataset JSON file
    input_text_file = "improved_transcription_result.txt"     # Path to the input text file
    preprocessed_video_dir = "videos"     # Directory containing preprocessed videos

    # Load the dataset
    if not os.path.exists(dataset_json_path):
        print(f"Dataset JSON file not found at {dataset_json_path}.")
        return

    wlasl_dataset = load_dataset(dataset_json_path)

    # Translate input text to video paths
    video_paths = translate_text_to_videos(input_text_file, wlasl_dataset, preprocessed_video_dir)

    if video_paths:
        # Combine videos into a single output
        output_video = create_sign_language_video(video_paths)
        if output_video:
            print(f"Translation video saved as {output_video}")
        else:
            print("Failed to create the output video.")
    else:
        print("No videos found for the input text.")

if __name__ == "__main__":
    main()
