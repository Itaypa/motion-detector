import cv2
import time
import multiprocessing

class Presentor(multiprocessing.Process):
    def __init__(self, detection_queue):
        super().__init__()
        self.detection_queue = detection_queue
        self.stop_event = multiprocessing.Event()

    def run(self):
        while not self.stop_event.is_set():
            if not self.detection_queue.empty():
                frame, detections = self.detection_queue.get()
                self.display_frame(frame, detections)

    def display_frame(self, frame, detections):
        if detections:
            for (x, y, w, h) in detections:
                #blurring detection
                roi = frame[y:y+h, x:x+w]
                blurred_roi = cv2.GaussianBlur(roi, (15, 15), 0)  
                frame[y:y+h, x:x+w] = blurred_roi
                #adding rectangle
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        cv2.putText(frame, f'Time: {time.strftime("%H:%M:%S")}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.stop()

    def stop(self):
        self.stop_event.set()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    detection_queue = multiprocessing.Queue()

    presentor = Presentor(detection_queue)
    presentor.start()
    presentor.join()
