import cv2
import ffmpeg
import os
from moviepy.editor import VideoFileClip

class VideoLoader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.metadata = self._extract_metadata()

    def _extract_metadata(self):
        probe = ffmpeg.probe(self.filepath)
        video_info = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
        return {
            'fps': eval(video_info['r_frame_rate']),
             'duration' : float(video_info['duration']),
            'width' : int(video_info['width']),
            'height': int(video_info['height'])
        }
    def extract_frames(self, output_dir, frame_rate=1): #frame rate is how many frames to save per second
        os.makedirs('cinematica/data/proceessed/'+output_dir, exist_ok=True)
        video = cv2.VideoCapture(self.filepath)
        fps = self.metadata['fps']
        frame_interval = fps/frame_rate #this is the interval for every frame saved
        count = 0
        saved_count = 0

        while True:
            ret, frame = video.read() #gets each frame
            if not ret:
                break
            if count % frame_interval == 0:
                cv2.imwrite(f"{output_dir}/frame_{saved_count:04d}.jpg", frame)
                saved_count += 1
            count += 1
        video.release() 
        return
    def extract_audio(self, audio_path):
        video_clip = VideoFileClip(self.filepath)
        audio = video_clip.audio
        audio.close()
        video_clip.close()

