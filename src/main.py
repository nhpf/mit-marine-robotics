import os

from tqdm import tqdm
from utils.video_proc import get_color_corrected_frames

# Define media directories
media_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "media")
input_media_dir = os.path.join(media_dir, "input")
output_media_dir = os.path.join(media_dir, "output")
frames_media_dir = os.path.join(media_dir, "frames")

# Check if directories exist
if not os.path.exists(input_media_dir):
    os.makedirs(input_media_dir)
    exit("No input media found in media/input, please add your MP4 files there")
if not os.path.exists(output_media_dir):
    os.makedirs(output_media_dir)
if not os.path.exists(frames_media_dir):
    os.makedirs(frames_media_dir)

# Process every mp4 file in media folder

# Get list of all mp4 files
mp4_file_names = [
    os.path.basename(file_path)
    for file_path in os.listdir(input_media_dir)
    if file_path.lower().endswith(".mp4")
]

if len(mp4_file_names) == 0:
    print("No MP4 files found in media/input!")
    exit()

for filename in tqdm(mp4_file_names, desc="Processing videos inside media/input"):
    frames_dir_path = os.path.join(frames_media_dir, os.path.splitext(filename)[0])
    if not os.path.exists(frames_dir_path):
        os.makedirs(frames_dir_path)

    # Save PNG sequence in frames_dir_path
    get_color_corrected_frames(
        video_path=os.path.join(input_media_dir, filename),
        output_dir=frames_dir_path,
        target_fps=2,
    )

    # process_video(
    #     input_video_path=os.path.join(input_media_dir, filename),
    #     output_video_path=os.path.join(output_media_dir, filename),
    # )
