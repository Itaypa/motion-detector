import cv2
import imutils
import multiprocessing

class Detector(multiprocessing.Process):
    def __init__(self, frame_queue, detection_queue):
        super().__init__()
        self.frame_queue = frame_queue
        self.detection_queue = detection_queue
        self.stop_event = multiprocessing.Event()
        self.min_contour_area = 500
        self.prev_frame = None

    def run(self):
        while not self.stop_event.is_set():
            if not self.frame_queue.empty():
                frame = self.frame_queue.get()
                if isinstance(frame, str) and frame == 'END':
                    print("Ended video, shutting down")
                    self.detection_queue.put(frame)
                    self.stop()
                    break
                detections = self.detect_motion(frame)
                self.detection_queue.put((frame, detections))

    def detect_motion(self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if self.prev_frame is None:
            self.prev_frame = gray_frame
            return []
        diff = cv2.absdiff(gray_frame, self.prev_frame)
        thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        self.prev_frame = gray_frame

        detections = []
        for contour in cnts:
            if cv2.contourArea(contour) < self.min_contour_area:
                continue
            (x, y, w, h) = cv2.boundingRect(contour)
            detections.append((x, y, w, h))

        return detections

    def stop(self):
        self.stop_event.set()

if __name__ == "__main__":
    frame_queue = multiprocessing.Queue()
    detection_queue = multiprocessing.Queue()

    detector = Detector(frame_queue, detection_queue)
    detector.start()
    detector.join()
