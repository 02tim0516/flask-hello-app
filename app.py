from flask import Flask, Response, render_template_string
import cv2

app = Flask(__name__)
camera_url = "https://trafficvideo2.tainan.gov.tw/54b2e135"

# 網頁模板：左側為影像，右側為學號/姓名/路口名稱
HTML_TEMPLATE = '''
<!doctype html>
<html>
<head>
    <title>台南即時交通監視器</title>
    <style>
        body { font-family: Arial; display: flex; margin: 0; }
        .video-container { flex: 2; padding: 20px; }
        .info-panel {
            flex: 1;
            background-color: #f8f8f8;
            padding: 20px;
            border-left: 1px solid #ccc;
        }
        h1 { margin-top: 0; }
        .info-item { margin-bottom: 20px; font-size: 18px; }
    </style>
</head>
<body>
    <div class="video-container">
        <h1>即時監視器畫面</h1>
        <img src="{{ url_for('video_feed') }}" width="100%">
    </div>
    <div class="info-panel">
        <div class="info-item"><strong>學號：</strong> M113</div>
        <div class="info-item"><strong>姓名：</strong> 我大爺</div>
        <div class="info-item"><strong>路口名稱：</strong> 台南市 中華西路與健康路</div>
    </div>
</body>
</html>
'''

def generate_frames():
    cap = cv2.VideoCapture(camera_url)
    if not cap.isOpened():
        raise RuntimeError("無法開啟攝影機串流")

    while True:
        success, frame = cap.read()
        if not success:
            cap.release()
            cap = cv2.VideoCapture(camera_url)
            continue

        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
