from flask import Flask, request, jsonify, send_file
import os
from run import run_triposr

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    image_name = data.get('image')
    if not image_name:
        return jsonify({'error': 'No image name provided'}), 400
    image_path = os.path.join(os.getcwd(), image_name)
    if not os.path.exists(image_path):
        return jsonify({'error': 'Image not found'}), 404
    result_path = run_triposr(image_path)
    # Assume the output is an image file (e.g., .png, .jpg, etc.)
    # If it's not, adjust the logic accordingly
    if not os.path.exists(result_path):
        return jsonify({'error': 'Output file not found'}), 500
    return send_file(result_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
