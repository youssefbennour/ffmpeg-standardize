import subprocess
import os
import shutil

def generate_non_standard_resolutions(input_video, output_dir, resolutions):
    shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    for width, height in resolutions:
        output_file = os.path.join(output_dir, f"{width}x{height}.mp4")
        try:
            command = [
                "ffmpeg",
                "-y",
                "-i", input_video,
                "-vf", f"scale={width}:{height}",
                output_file
            ]
            subprocess.run(command, check=True)
            print(f"Generated video: {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to generate resolution {width}x{height}: {e}")

if __name__ == "__main__":
    input_video = "input.mp4"  

    output_dir = "output_videos"

    non_standard_resolutions = [
        (854, 476),  
        (642, 358),  
        (1250, 720), 
        (1918, 1080),
        (2558, 1438),
        (3838, 2158),
    ]

    generate_non_standard_resolutions(input_video, output_dir, non_standard_resolutions)

