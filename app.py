from flask import Flask, render_template, request, jsonify
import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image  # added for handling webcam image blobs

# Import chatbot function
from chatbot import get_chatbot_response

app = Flask(__name__)

# Load the trained traffic sign model
model = load_model("traffic_sign_model.h5")

# Class mapping
classes_names = {
    0: 'Speed limit (20km/h)',
    1: 'Speed limit (30km/h)',
    2: 'Speed limit (50km/h)',
    3: 'Speed limit (60km/h)',
    4: 'Speed limit (70km/h)',
    5: 'Speed limit (80km/h)',
    6: 'End of speed limit (80km/h)',
    7: 'Speed limit (100km/h)',
    8: 'Speed limit (120km/h)',
    9: 'No passing',
    10: 'No passing vehicles > 3.5 tons',
    11: 'Right-of-way at intersection',
    12: 'Priority road',
    13: 'Yield',
    14: 'Stop',
    15: 'No vehicles',
    16: 'Vehicles > 3.5 tons prohibited',
    17: 'No entry',
    18: 'General caution',
    19: 'Dangerous curve left',
    20: 'Dangerous curve right',
    21: 'Double curve',
    22: 'Bumpy road',
    23: 'Slippery road',
    24: 'Road narrows on the right',
    25: 'Road work',
    26: 'Traffic signals',
    27: 'Pedestrians',
    28: 'Children crossing',
    29: 'Bicycles crossing',
    30: 'Beware of ice/snow',
    31: 'Wild animals crossing',
    32: 'End speed + passing limits',
    33: 'Turn right ahead',
    34: 'Turn left ahead',
    35: 'Ahead only',
    36: 'Go straight or right',
    37: 'Go straight or left',
    38: 'Keep right',
    39: 'Keep left',
    40: 'Roundabout mandatory',
    41: 'End of no passing',
    42: 'End no passing vehicles > 3.5 tons'
}

# Prediction function (for file upload)
def predict_sign(img_path):
    img = cv2.imread(img_path)
    img = cv2.resize(img, (32, 32))
    img = np.expand_dims(img, axis=0) / 255.0
    pred = model.predict(img)[0]
    class_index = np.argmax(pred)
    confidence = pred[class_index] * 100
    return classes_names[class_index], round(confidence, 2)


# Homepage (Upload + Chatbot)
@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    confidence = None
    chat_response = None
    file_path = None

    if request.method == "POST":
        # If user uploaded an image
        if "file" in request.files and request.files["file"].filename != "":
            file = request.files["file"]

            upload_folder = os.path.join("static", "uploads")
            os.makedirs(upload_folder, exist_ok=True)

            file_path = os.path.join(upload_folder, file.filename)
            file.save(file_path)

            prediction, confidence = predict_sign(file_path)

        # If user sent a chat message
        elif "message" in request.form:
            user_message = request.form["message"]
            chat_response = get_chatbot_response(user_message)

    return render_template(
        "index.html",
        prediction=prediction,
        confidence=confidence,
        chat_response=chat_response,
        file_path=file_path
    )


# Chatbot API route
@app.route("/chatbot", methods=["POST"])
def chatbot_api():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"response": "Please enter a message."})

    response = get_chatbot_response(user_message)
    return jsonify({"response": response})


# Camera page
@app.route("/camera")
def camera():
    return render_template("camera.html")


# Prediction route for camera capture
@app.route("/predict_camera", methods=["POST"])
def predict_camera():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    file_path = os.path.join("static/uploads", file.filename)
    os.makedirs("static/uploads", exist_ok=True)
    file.save(file_path)

    result, confidence = predict_sign(file_path)

    # Cast confidence to float to fix JSON serialization error
    return jsonify({
        "result": result,
        "confidence": float(confidence)
    })



if __name__ == "__main__":
    app.run(debug=True)
