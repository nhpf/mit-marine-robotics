# This code is based on an example from bornfree's GitHub repository.
# Original code: https://github.com/bornfree/dive-color-corrector/blob/main/correct.py
# Modifications were made to adapt it to our specific needs.

import math
from typing import Generator

import cv2
import numpy as np
from tqdm import tqdm

from .color_correcting import _apply_filter, _get_filter_matrix, correct_img

SAMPLE_SECONDS = 2  # Extracts color correction from every N seconds


def _analyze_video(input_video_path: str, output_video_path: str) -> Generator:
    # Initialize new video writer
    cap = cv2.VideoCapture(input_video_path)
    fps = math.ceil(cap.get(cv2.CAP_PROP_FPS))
    frame_count = math.ceil(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Get filter matrices for every 10th frame
    filter_matrix_indexes = []
    filter_matrices = []
    count = 0

    print("Analyzing...")
    while cap.isOpened():
        count += 1
        print(f"{count} frames", end="\r")
        ret, frame = cap.read()
        if not ret:
            # End video read if we have gone beyond reported frame count
            if count >= frame_count:
                break

            # Failsafe to prevent an infinite loop
            if count >= 1e6:
                break

            # Otherwise this is just a faulty frame read, try reading next frame
            continue

        # Pick filter matrix from every N seconds
        if count % (fps * SAMPLE_SECONDS) == 0:
            mat = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            filter_matrix_indexes.append(count)
            filter_matrices.append(_get_filter_matrix(mat))

        yield count

    cap.release()

    # Build a interpolation function to get filter matrix at any given frame
    filter_matrices = np.array(filter_matrices)

    yield {
        "input_video_path": input_video_path,
        "output_video_path": output_video_path,
        "fps": fps,
        "frame_count": count,
        "filters": filter_matrices,
        "filter_indices": filter_matrix_indexes,
    }


def process_video(input_video_path: str, output_video_path: str) -> None:
    video_data = dict()
    for item in _analyze_video(input_video_path, output_video_path):
        if isinstance(item, dict):
            video_data = item

    cap = cv2.VideoCapture(video_data["input_video_path"])

    frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    new_video = cv2.VideoWriter(
        video_data["output_video_path"],
        fourcc,
        video_data["fps"],
        (int(frame_width), int(frame_height)),
    )

    filter_matrices = video_data["filters"]
    filter_indices = video_data["filter_indices"]

    filter_matrix_size = len(filter_matrices[0])

    def get_interpolated_filter_matrix(frame_number):
        return [
            np.interp(frame_number, filter_indices, filter_matrices[..., x])
            for x in range(filter_matrix_size)
        ]

    print("Processing...")

    frame_count = video_data["frame_count"]

    count = 0
    cap = cv2.VideoCapture(video_data["input_video_path"])
    while cap.isOpened():
        count += 1
        percent = 100 * count / frame_count
        print("{:.2f}".format(percent), end=" % \r")
        ret, frame = cap.read()

        if not ret:
            # End video read if we have gone beyond reported frame count
            if count >= frame_count:
                break

            # Failsafe to prevent an infinite loop
            if count >= 1e6:
                break

            # Otherwise this is just a faulty frame read, try reading next
            continue

        # Apply the filter
        rgb_mat = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        interpolated_filter_matrix = get_interpolated_filter_matrix(count)
        corrected_mat = _apply_filter(rgb_mat, interpolated_filter_matrix)
        corrected_mat = cv2.cvtColor(corrected_mat, cv2.COLOR_RGB2BGR)

        new_video.write(corrected_mat)

    cap.release()
    new_video.release()


def get_color_corrected_frames(
    video_path: str, output_dir: str, target_fps: int
) -> None:
    cap = cv2.VideoCapture(video_path)
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = math.ceil(original_fps / target_fps)
    frame_count = math.ceil(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    count = 0
    output_count = 0

    # Use tqdm to track progress
    with tqdm(
        total=frame_count, desc="Generating color corrected frames", unit="frame"
    ) as pbar:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Save the frame if it's one of the frames we want to keep
            if count % frame_interval == 0:
                corrected_frame = correct_img(frame)

                output_count += 1
                output_count_str = str(output_count).zfill(6)
                cv2.imwrite(f"{output_dir}/{output_count_str}.png", corrected_frame)

            count += 1
            pbar.update(1)

    cap.release()
    print(f"PNG sequence creation complete for {video_path}\n\n")
