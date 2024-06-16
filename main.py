import multiprocessing
from streamer.streamer import Streamer
from detector.detector import Detector
from presentor.presentor import Presentor

def main(video_path):
    frame_queue = multiprocessing.Queue()
    detection_queue = multiprocessing.Queue()

    streamer = Streamer(video_path, frame_queue)
    detector = Detector(frame_queue, detection_queue)
    displayer = Presentor(detection_queue)

    streamer.start()
    detector.start()
    displayer.start()

    streamer.join()
    detector.join()
    displayer.join()

if __name__ == "__main__":
    main("test_video.mp4")
