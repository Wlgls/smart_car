def gen(camera):
    while True:
        frame = camera.get_frame().tobytes()
        yield (b"--frame\r\n"
                b"Content-Type:image/jpeg\r\n\r\n" + frame + b"\r\n")
@app.route("/video_feed")
def video_feed():
    return Response(gen(Camera()), 
            mimetype="multipart/x-mixed-replace;boundary=frame")