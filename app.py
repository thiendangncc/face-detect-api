import cv2
import mediapipe as mp
import numpy as np
import base64
from flask import Flask, request, jsonify

# Initialize Mediapipe Face Detection
mp_face_detection = mp.solutions.face_detection

# Initialize Flask App
app = Flask(__name__)

# Load Mediapipe Face Detection Model
face_detection = mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)

@app.route('/detect', methods=['POST'])
def detect_faces():
    try:
        # Parse JSON request
        data = request.json
        if not data or 'image' not in data:
            return jsonify({"error": "No image data provided"}), 400

        # Decode base64 image
        image_data = base64.b64decode(data['image'])
        np_arr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Convert image to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Detect faces
        results = face_detection.process(rgb_image)
        if not results.detections:
            return jsonify({"message": "No faces detected"}), 200

        # Process detections
        faces = []
        for detection in results.detections:
            bbox = detection.location_data.relative_bounding_box
            faces.append({
                "x": bbox.xmin,
                "y": bbox.ymin,
                "width": bbox.width,
                "height": bbox.height,
                "confidence": detection.score[0]
            })

        return jsonify({"faces": faces})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
