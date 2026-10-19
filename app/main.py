from app.VideoStream import VideoStream
from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import time

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

camera = VideoStream(source="media/sample.mp4")

@app.get("/")
def test():
    return FileResponse("static/index.html")

@app.get("/video_feed")
def video_feed():
    return StreamingResponse(
        mjpeg_generator(), 
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

def mjpeg_generator():
    while True:
        frame_bytes = camera.get_jpg_frame()

        if frame_bytes:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        time.sleep(0.03)
        