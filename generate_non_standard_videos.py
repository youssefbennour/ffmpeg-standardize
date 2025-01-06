import subprocess
import os
import shutil
def get_video_resolution(file_path):
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

def generate_non_standard_resolutions(input_video, output_dir):
    if(os.path.exists(output_dir)):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    width, height = get_video_resolution(input_video)
    for h in range(1080, 1444, 4):
        output_file = os.path.join(output_dir, f"{width}x{h}.mp4")
        try:
            command = [
                "ffmpeg",
                "-y",
                "-i", input_video,
                "-vf", f"scale={width}:{h}",
                output_file
            ]
            subprocess.run(command, check=True)
            print(f"Generated video: {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to generate resolution {width}x{h}: {e}")

if __name__ == "__main__":
    input_video = "input.mp4"  

    output_dir = "output_videos"
    generate_non_standard_resolutions(input_video, output_dir)


