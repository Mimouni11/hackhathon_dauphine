import subprocess
import os

def run_blender_animation(blender_exe_path, blender_file_path, blender_script_path, keypoints_json_path, output_video_path):
    blender_command = [
        blender_exe_path,
        '--background',  # Run in background (no UI)
        blender_file_path,
        '--python', blender_script_path,
        '--',
        keypoints_json_path,
        output_video_path
    ]

    try:
        subprocess.run(blender_command, check=True)
        print(f"Animation rendered successfully and saved to {output_video_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during Blender execution: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Example Usage
if __name__ == '__main__':
    blender_exe_path = 'C:/Program Files/Blender Foundation/Blender 4.0/blender.exe'
    blender_file_path = 'C:/Users/mimou/OneDrive/Desktop/hackhathon/untitled.blend'
    blender_script_path = 'C:/Users/mimou/OneDrive/Desktop/hackhathon/animate_avatar.py'
    keypoints_json_path = 'C:/Users/mimou/OneDrive/Desktop/hackhathon/keypoints_data.json'
    output_video_path = 'C:/Users/mimou/OneDrive/Desktop/hackhathon/output_with_avatar.mp4'

    run_blender_animation(blender_exe_path, blender_file_path, blender_script_path, keypoints_json_path, output_video_path)
