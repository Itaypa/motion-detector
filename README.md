# Video Motion Detection System

This project is a video motion detection system using Python and OpenCV. It captures video frames, detects motion, and displays the results with visual indicators.

## Features

- **Frame Capture:** Continuously captures video frames from a specified video file.
- **Motion Detection:** Analyzes frames to detect motion based on changes between frames.
- **Frame Display:** Displays the video frames with detected motion highlighted.
- **Multiprocessing:** Utilizes Python's `multiprocessing` library to run frame capture, motion detection, and display concurrently.

## File Overview

- **main.py:** The main entry point of the application, coordinating the different components.
- **streamer.py:** Captures video frames from the specified video file and places them in a queue.
- **detector.py:** Detects motion in video frames by comparing consecutive frames and identifies areas of movement.
- **presentor.py:** Displays the video frames with detected motion highlighted, blurring the areas of movement.

## Dependencies

- Python 3.x
- OpenCV
- imutils

Install the required dependencies using pip:

```bash
pip install opencv-python imutils


Caveats
Choice of Queues for Process Communication
The decision to use queues for communication between processes in this project was made to enhance scalability and manage overhead effectively. Queues provide a thread-safe mechanism to exchange data between processes, allowing for a clean separation of concerns and better control over the flow of data.

Scalability
Using queues allows each component (Streamer, Detector, Presentor) to be scaled independently based on their resource requirements. For instance, the Detector might be designed to utilize a GPU for enhanced performance. By isolating the detector process and communicating via queues, multiple instances of the detector can be run on separate GPUs or even separate machines if needed, without impacting the streamer or presentor processes.

Load Balancing
This architecture also facilitates load balancing. If the motion detection process becomes a bottleneck, additional detector instances can be added to handle the load, while the streamer continues to operate with minimal overhead. Similarly, the presentor can be scaled independently based on the display requirements.

Resource Optimization
Queues help in optimizing resource usage. The streamer, which primarily uses CPU resources to read video frames, can run independently from the detector, which might require heavy GPU resources. This separation ensures that the CPU and GPU resources are utilized efficiently and do not interfere with each other, leading to better overall performance.

Example Scenario
Consider a scenario where the Detector process requires GPU acceleration for real-time performance. The streamer, on the other hand, only needs CPU resources to read video frames. By using queues, the streamer can continuously feed frames to the detector, which processes them at its own pace. If the detection workload increases, additional GPU-equipped detector instances can be deployed, each processing frames from the queue, thereby distributing the workload and maintaining real-time performance.