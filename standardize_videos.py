import os
import re
import subprocess
from colorama import Fore, Back, Style
from math import sqrt

class StandardResolution:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def distance_to(self, width, height):
        return sqrt((self.width - width) ** 2 + (self.height - height) ** 2)

def get_closest_standard_resolution(resolutions, width, height):
    return min(
       [resolution for resolution in resolutions if resolution.height < height], 
        key=lambda res: res.distance_to(width, height))

def crop_or_pad_video(input_file, output_file, original_width, original_height, target_width, target_height):
    print(Back.GREEN + f"orignial resolution : {original_width}x{original_height}")
    print(Back.GREEN + f"target resolution : {target_width}x{target_height}")
    
    filter_str = ""
    if original_height > target_height or original_width > target_width:
        original_width = target_width if original_width > target_width else original_width
        original_height = target_height if original_height > target_height else original_height
        filter_str += f"crop={original_width}:{original_height}"
        if original_height < target_height or original_width < target_width:
            filter_str += ","
    if original_height < target_height or original_width < target_width:
        original_width = target_width if original_width < target_width else original_width
        original_height = target_height if original_height < target_height else original_height
        filter_str += f"pad={original_width}:{original_height}:-1:-1"
    
    # Run FFmpeg
    command = [
        "ffmpeg",
        "-y",
        "-i", input_file,
        "-vf", filter_str,
        output_file
    ]
    print(Back.GREEN + f"FFMPEG command : {command}")
    subprocess.run(command, check=True)

def process_videos(output_dir):
    standard_resolutions = [
        StandardResolution(1920, 1080),  # 1080p
        StandardResolution(1280, 720),  # 720p
        StandardResolution(854, 480),   # 480p
        StandardResolution(640, 360),   # 360p
        StandardResolution(426, 240)    # 240p
    ]

    filename_regex = re.compile(r"(\d+)x(\d+)\.mp4")

    for filename in os.listdir(output_dir):
        match = filename_regex.match(filename)
        if match:
            width, height = map(int, match.groups())
            input_file = os.path.join(output_dir, filename)

            closest_resolution = get_closest_standard_resolution(standard_resolutions, width, height)
            print(f"Processing {filename}: Closest resolution is {closest_resolution.width}x{closest_resolution.height}")

            output_file = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_standardized.mp4")
            crop_or_pad_video(input_file, output_file, width, height,closest_resolution.width, closest_resolution.height)
            print(f"Generated standardized video: {output_file}")

if __name__ == "__main__":
    output_dir = "output_videos"

    process_videos(output_dir)
