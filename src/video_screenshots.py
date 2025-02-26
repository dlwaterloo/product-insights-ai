import cv2
import os
import json
from pathlib import Path

def parse_timestamp(timestamp):
    """Convert MM:SS timestamp to seconds"""
    minutes, seconds = map(int, timestamp.split(':'))
    return minutes * 60 + seconds

def extract_screenshots_from_json(video_path, json_path, output_folder):
    """Extract screenshots from video based on timestamps in JSON data"""
    # Create output directory if it doesn't exist
    output_dir = Path(output_folder)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Open the video file
    video = cv2.VideoCapture(str(video_path))
    
    if not video.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return
    
    # Get video properties
    fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Read the JSON analysis
    with open(json_path, 'r') as f:
        json_data = json.load(f)
    
    # Process each step from the JSON
    for step in json_data['workflow_steps']:
        timestamp = step['timestamp']
        description = step['description']
        is_major = step['is_major_step']
        
        # Convert timestamp to frame number
        seconds = parse_timestamp(timestamp)
        frame_number = int(seconds * fps)
        
        # Set video to the correct frame
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        success, frame = video.read()
        
        if success:
            # Create filename with timestamp and truncated description
            description_slug = description.lower().replace(' ', '_')[:30]
            filename = f"{timestamp.replace(':', '_')}_{description_slug}.png"
            if is_major:
                filename = f"major_{filename}"
            
            screenshot_path = output_dir / filename
            cv2.imwrite(str(screenshot_path), frame)
            print(f"Saved screenshot at {screenshot_path}")
        else:
            print(f"Failed to capture frame at timestamp {timestamp}")
    
    video.release()
    print("\nScreenshot extraction complete!")

if __name__ == "__main__":
    video_file = Path("input/your_video.mp4")
    json_file = Path("temp/analysis.json")
    output_folder = Path("temp/screenshots")
    
    extract_screenshots_from_json(video_file, json_file, output_folder)
