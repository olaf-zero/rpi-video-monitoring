from app.video_stream import VideoStream
from app.telemetry import get_system_stats

from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from fastapi import HTTPException

import time


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

camera = VideoStream(source=0) # "media/sample.mp4" - testowy plik.mp4; 0 - obraz z domyślnej kamery

@app.get("/")
def test():
    return FileResponse("static/index.html")


@app.get("/video_feed")
def video_feed():
    return StreamingResponse(
        mjpeg_generator(), 
        media_type="multipart/x-mixed-replace; boundary=frame"
    )


@app.get("/api/telemetry")
def telemetry():
    return get_system_stats()


@app.post("/api/snapshot")
def take_snapshot():
    file_name = camera.get_snapshot()

    if file_name == None:
        raise HTTPException(status_code=500, detail="Nie udało się zapisać klatki.")
    else:
        return {"status": "ok", "file_name": file_name}


def mjpeg_generator():
    while True:
        frame_bytes = camera.get_jpg_frame()

        if frame_bytes:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        time.sleep(0.03)
        