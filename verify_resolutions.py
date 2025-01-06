import os
import subprocess
import re

class StandardResolution:
    """Class representing a standard video resolution."""
    def __init__(self, width, height):
        self.width = width
        self.height = height

def get_video_resolution(file_path):
    """
    Use ffprobe to get the resolution of a video.
    
    Args:
        file_path (str): Path to the video file.

    Returns:
        tuple: Width and height of the video (int, int).
    """
    command = [
        "ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", 
        "stream=width,height", "-of", "csv=p=0", file_path
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed for {file_path}: {result.stderr}")
    
    # Extract width and height
    width, height = map(int, result.stdout.strip().split(","))
    return width, height

def is_standard_resolution(width, height, standard_resolutions):
    """
    Check if the given width and height match any standard resolution.
    
    Args:
        width (int): Video width.
        height (int): Video height.
        standard_resolutions (list of StandardResolution): List of standard resolutions.

    Returns:
        bool: True if the resolution is standard, False otherwise.
    """
    for res in standard_resolutions:
        if res.width == width and res.height == height:
            return True
    return False

def validate_videos(output_dir):
    """
    Validate if all standardized videos in the directory have standard resolutions.
    
    Args:
        output_dir (str): Directory containing the standardized videos.
    """
    # List of standard resolutions
    standard_resolutions = [
        StandardResolution(1920, 1080),  # 1080p
        StandardResolution(1280, 720),  # 720p
        StandardResolution(854, 480),   # 480p
        StandardResolution(640, 360),   # 360p
        StandardResolution(426, 240)    # 240p
    ]

    for filename in os.listdir(output_dir):
        # Skip non-MP4 files
        if not filename.endswith("standardized.mp4"):
            continue
        
        file_path = os.path.join(output_dir, filename)
        
        try:
            width, height = get_video_resolution(file_path)
            if is_standard_resolution(width, height, standard_resolutions):
                print(f"{filename}: Resolution is standard ({width}x{height}).")
            else:
                print(f"{filename}: Resolution is NOT standard ({width}x{height}).")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    # Directory containing the standardized videos
    output_dir = "output_videos"

    # Validate video resolutions
    validate_videos(output_dir)

