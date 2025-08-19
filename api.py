from flask import Flask, request, jsonify
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
    result = run_triposr(image_path)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
