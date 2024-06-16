import cv2
import multiprocessing

class Streamer(multiprocessing.Process):
    def __init__(self, video_path, frame_queue):
        super().__init__()
        self.video_path = video_path
        self.frame_queue = frame_queue
        print(f"video_path={video_path}, frame_queue={frame_queue}")
        self.stop_event = multiprocessing.Event()

    def run(self):
        print(f"stratring video capturing")
        cap = cv2.VideoCapture(self.video_path)
        while not self.stop_event.is_set():
            ret, frame = cap.read()
            if not ret:
                break            
            self.frame_queue.put(frame)
        cap.release()

    def stop(self):
        self.stop_event.set()

if __name__ == "__main__":
    video_path = "test_video.mp4" 
    frame_queue = multiprocessing.Queue()

    streamer = Streamer(video_path, frame_queue)
    streamer.start()
    streamer.join()
