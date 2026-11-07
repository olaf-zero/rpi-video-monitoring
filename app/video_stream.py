import cv2
import threading
import time
import os

from datetime import datetime

class VideoStream:
    def __init__(self, source = "media/sample.mp4"):
        self.source = source

        self.cap = cv2.VideoCapture(self.source)
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.target_fps = fps if fps and fps > 0 else 30.0

        self.running = True
        self.current_frame = None

        self.lock = threading.Lock() # mutex to block acces to self.current_frame

        # constant updating fo self.current_frame
        self.camera_thread = threading.Thread(target=self._update_frame, daemon=True)
        self.camera_thread.start()

        os.makedirs("media", exist_ok=True)


    def get_jpg_frame(self):
        with self.lock:
            if self.current_frame is None: 
                return None

            frame = self.current_frame.copy()

        converted, jpg_frame = cv2.imencode(".jpg", frame)

        return jpg_frame.tobytes() if converted else None


    def get_snapshot(self):
        with self.lock:
            if self.current_frame is None:
                return None

            frame = self.current_frame.copy()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"snap_{timestamp}.jpg"

        file_path = os.path.join("media", file_name)

        ret = cv2.imwrite(filename=file_path, img=frame)

        return file_name if ret else None


    def _update_frame(self):
        while self.running:
            # measuring execution time of the code for more accurate fps
            start_time = time.perf_counter()

            ret, frame = self.cap.read()

            # restart video if it has ended (if using video as a source)
            if not ret:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

                _, frame = self.cap.read()

            with self.lock:
                self.current_frame = frame

            end_time = time.perf_counter()

            sleep_time = max((1.0 / self.target_fps) - (end_time - start_time), 0)

            time.sleep(sleep_time)
