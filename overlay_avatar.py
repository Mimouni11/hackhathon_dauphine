# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 15:42:16 2024

@author: mimou
"""

import cv2
import numpy as np

def overlay_avatar_on_video(original_video_path, avatar_animation_path, output_video_path):
    # Open the original video
    cap_video = cv2.VideoCapture(original_video_path)
    # Open the transparent video (avatar animation)
    cap_avatar = cv2.VideoCapture(avatar_animation_path)

    # Get the video properties (ensure both videos have the same frame size and rate)
    frame_width = int(cap_video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap_video.get(cv2.CAP_PROP_FPS))

    # Define codec and create a VideoWriter object to save the final output
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    while cap_video.isOpened() and cap_avatar.isOpened():
        ret_video, frame_video = cap_video.read()
        ret_avatar, frame_avatar = cap_avatar.read()

        if not ret_video or not ret_avatar:
            break

        # Resize the avatar frame to fit the video (optional)
        frame_avatar = cv2.resize(frame_avatar, (frame_width, frame_height))

        # Make sure the avatar frame has an alpha channel (transparency)
        if frame_avatar.shape[2] == 4:  # Ensure alpha channel exists
            alpha_channel = frame_avatar[:, :, 3] / 255.0  # Normalize alpha to [0, 1]

            # Blend the frames: combine based on alpha channel (transparency)
            for c in range(0, 3):  # Loop over each color channel
                frame_video[:, :, c] = frame_video[:, :, c] * (1 - alpha_channel) + frame_avatar[:, :, c] * alpha_channel

        # Write the resulting frame to the output video
        out.write(frame_video)

    cap_video.release()
    cap_avatar.release()
    out.release()

# Example usage
original_video_path = 'output_translation.mp4'  # Path to the original video
avatar_animation_path = 'avatar_animation.webm'  # Path to the transparent avatar animation
output_video_path = 'output_with_overlay.mp4'  # Path to save the final video

overlay_avatar_on_video(original_video_path, avatar_animation_path, output_video_path)
