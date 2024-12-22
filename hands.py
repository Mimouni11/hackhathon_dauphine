from vpython import sphere, cylinder, vector, rate, canvas, color, box

# Load keypoints data
def load_keypoints(json_path):
    import json
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Initialize the avatar (hand joints, bones, and static body parts)
def create_avatar():
    # Create spheres for hand joints
    joints = [sphere(radius=0.2, color=color.green) for _ in range(21)]

    # Create cylinders for hand bones (20 bones connecting 21 joints)
    bones = [cylinder(radius=0.1, color=color.white) for _ in range(20)]

    # Create static body parts
    head = sphere(radius=1, color=color.yellow, pos=vector(0, 8, 0))
    torso = box(size=vector(2, 4, 1), color=color.blue, pos=vector(0, 4, 0))
    left_upper_arm = cylinder(radius=0.3, color=color.red, pos=vector(-1.5, 6, 0), axis=vector(-1, -1.5, 0))
    right_upper_arm = cylinder(radius=0.3, color=color.red, pos=vector(1.5, 6, 0), axis=vector(1, -1.5, 0))
    left_forearm = cylinder(radius=0.2, color=color.red, pos=vector(-2.5, 4.5, 0), axis=vector(0, -1, 0))
    right_forearm = cylinder(radius=0.2, color=color.red, pos=vector(2.5, 4.5, 0), axis=vector(0, -1, 0))

    # Return hand parts and static parts
    return joints, bones, [head, torso, left_upper_arm, right_upper_arm, left_forearm, right_forearm]

# Update the avatar for each frame
def update_avatar(joints, bones, keypoints, scale_factor=5):
    for i, joint in enumerate(joints):
        if i < len(keypoints):
            x, y, z = keypoints[i]
            joint.pos = vector(x * scale_factor, y * scale_factor, z * scale_factor)

    # Update bone positions
    bone_connections = [
        (0, 1), (1, 2), (2, 3), (3, 4),  # Thumb
        (0, 5), (5, 6), (6, 7), (7, 8),  # Index finger
        (0, 9), (9, 10), (10, 11), (11, 12),  # Middle finger
        (0, 13), (13, 14), (14, 15), (15, 16),  # Ring finger
        (0, 17), (17, 18), (18, 19), (19, 20)  # Pinky finger
    ]

    for i, (start, end) in enumerate(bone_connections):
        if start < len(keypoints) and end < len(keypoints):
            bones[i].pos = joints[start].pos
            bones[i].axis = joints[end].pos - joints[start].pos

# Visualize hand keypoints with a static body as an avatar
def visualize_hand_keypoints(keypoints_data, scale_factor=5, frame_rate=15):
    # Create a VPython canvas with a light background
    canvas(title="Hand Gesture Avatar", width=800, height=600, background=color.gray(0.2), center=vector(0, 4, 0))

    # Add lighting for better visibility
    from vpython import distant_light
    distant_light(direction=vector(0, 0, -1), color=color.white)
    distant_light(direction=vector(0, 0, 1), color=color.white)

    # Create avatar parts
    joints, bones, static_parts = create_avatar()

    # Animate keypoints frame by frame
    for frame in keypoints_data:
        rate(frame_rate)  # Control animation speed

        if frame["hands"]:  # Check if hands data is present
            hand_keypoints = frame["hands"][0]  # Use the first hand for simplicity
            update_avatar(joints, bones, hand_keypoints, scale_factor)

# Main program
if __name__ == "__main__":
    keypoints_data = load_keypoints("hand_keypoints_data.json")
    visualize_hand_keypoints(keypoints_data, scale_factor=10, frame_rate=15)
