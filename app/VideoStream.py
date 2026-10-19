import cv2

class VideoStream:
    def __init__(self, source = "media/sample.mp4"):
        self.source = source
        self.cap = cv2.VideoCapture(self.source)

    def get_jpg_frame(self):
        for _ in range(2):
            ret, frame = self.cap.read()

            if ret:
                converted, jpg_frame = cv2.imencode(".jpg", frame)
                if converted:
                    return jpg_frame.tobytes()
                else:
                    return None
            else:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        return None