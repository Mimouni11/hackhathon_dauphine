import bpy
import json
import sys
from mathutils import Euler

# Load keypoints data
def load_keypoints(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Map MediaPipe keypoints to avatar arm and hand bones
def get_bone_name(pose_index, is_left=True):
    bone_mapping = {
        # Upper body and arms
        11: "mixamorig:LeftShoulder" if is_left else "mixamorig:RightShoulder",
        12: "mixamorig:LeftArm" if is_left else "mixamorig:RightArm",
        13: "mixamorig:LeftForeArm" if is_left else "mixamorig:RightForeArm",
        14: "mixamorig:LeftHand" if is_left else "mixamorig:RightHand",

        # Fingers
        15: "mixamorig:LeftHandThumb1" if is_left else "mixamorig:RightHandThumb1",
        16: "mixamorig:LeftHandThumb2" if is_left else "mixamorig:RightHandThumb2",
        17: "mixamorig:LeftHandIndex1" if is_left else "mixamorig:RightHandIndex1",
        18: "mixamorig:LeftHandIndex2" if is_left else "mixamorig:RightHandIndex2",
        19: "mixamorig:LeftHandMiddle1" if is_left else "mixamorig:RightHandMiddle1",
        20: "mixamorig:LeftHandMiddle2" if is_left else "mixamorig:RightHandMiddle2",
    }
    return bone_mapping.get(pose_index)

# Animate the avatar
def animate_avatar(keypoints_data, armature_name, output_video_path):
    armature = bpy.data.objects.get(armature_name)
    if not armature:
        print(f"Error: Armature '{armature_name}' not found!")
        return

    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')

    scale_factor = 5  # Adjust for Blender's world space

    for frame_number, frame_data in enumerate(keypoints_data):
        bpy.context.scene.frame_set(frame_number)
        print(f"Animating frame {frame_number}")

        # Animate upper body and hands
        if 'pose' in frame_data:
            for pose_index, keypoint in enumerate(frame_data['pose']):
                is_left = pose_index in [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
                bone_name = get_bone_name(pose_index, is_left=is_left)
                if not bone_name:
                    continue

                bone = armature.pose.bones.get(bone_name)
                if not bone:
                    print(f"Warning: Bone '{bone_name}' not found in armature. Skipping.")
                    continue

                try:
                    x, y, z = keypoint
                    bone.rotation_mode = 'XYZ'
                    bone.rotation_euler = Euler((x * scale_factor, y * scale_factor, z * scale_factor), 'XYZ')
                    bone.keyframe_insert(data_path="rotation_euler", frame=frame_number)
                except Exception as e:
                    print(f"Error animating bone '{bone_name}': {e}")

    bpy.ops.object.mode_set(mode='OBJECT')

    # Configure render settings
    camera = bpy.data.objects.get('Camera') or bpy.ops.object.camera_add()
    camera = bpy.context.view_layer.objects.active
    bpy.context.scene.camera = camera
    camera.location = (5, -5, 5)
    camera.rotation_euler = (1.1, 0, 0.8)

    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = len(keypoints_data)
    bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
    bpy.context.scene.render.ffmpeg.format = 'MPEG4'
    bpy.context.scene.render.ffmpeg.codec = 'H264'
    bpy.context.scene.render.filepath = output_video_path

    # Render animation
    bpy.ops.render.render(animation=True)
    print(f"Animation rendered and saved at {output_video_path}")

# Main entry point
if __name__ == '__main__':
    args = sys.argv[sys.argv.index('--') + 1:]
    if len(args) < 2:
        print("Usage: blender -b <blend_file> --python animate_avatar.py -- <keypoints_json_path> <output_video_path>")
        sys.exit(1)

    keypoints_json_path = args[0]
    output_video_path = args[1]

    keypoints_data = load_keypoints(keypoints_json_path)
    animate_avatar(keypoints_data, 'Armature', output_video_path)
