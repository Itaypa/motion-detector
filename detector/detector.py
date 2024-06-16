import cv2
import multiprocessing

class Detector(multiprocessing.Process):
    def __init__(self, frame_queue, detection_queue):
        super().__init__()
        self.frame_queue = frame_queue
        self.detection_queue = detection_queue
        self.stop_event = multiprocessing.Event()
        self.first_frame = None

    def run(self):
        while not self.stop_event.is_set():
            if not self.frame_queue.empty():
                frame = self.frame_queue.get()
                detections = self.detect_motion(frame)
                self.detection_queue.put((frame, detections))

    def detect_motion(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if self.first_frame is None:
            self.first_frame = gray
            return None

        frame_delta = cv2.absdiff(self.first_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        detections = []
        for contour in contours:
            if cv2.contourArea(contour) < 500:
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
