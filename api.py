from flask import Flask, request, jsonify, send_file, after_this_request
import os
import io
import requests
import uuid
from run import run_triposr

app = Flask(__name__)

@app.route('/api/convert/3D', methods=['POST'])
def predict():
    data = request.get_json()
    image_url = data.get('image_url')
    if not image_url:
        return jsonify({'error': 'No image_url provided'}), 400

    # Generate random filenames for input and output
    unique_id = str(uuid.uuid4())
    input_filename = f"input_{unique_id}.png"
    output_filename = f"mesh_{unique_id}.obj"
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)
    input_path = os.path.join(output_dir, input_filename)
    output_path = os.path.join(output_dir, output_filename)

    # Download the image
    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        with open(input_path, 'wb') as f:
            f.write(response.content)
    except Exception as e:
        return jsonify({'error': f'Failed to download image: {str(e)}'}), 400

    # Run the model
    result_path = run_triposr(
        image_path=input_path,
        output_dir=output_dir,
        input_filename=input_filename,
        output_filename=output_filename
    )

    # Return the .obj file as response
    if not os.path.exists(result_path):
        # Clean up input if output failed
        if os.path.exists(input_path):
            os.remove(input_path)
        return jsonify({'error': 'Output file not found'}), 500

    # Read the .obj file into memory
    obj_buffer = io.BytesIO()
    with open(result_path, 'rb') as f:
        obj_buffer.write(f.read())
    obj_buffer.seek(0)

    # Clean up files before returning
    try:
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(result_path):
            os.remove(result_path)
    except Exception:
        pass

    # Set a default filename for the .obj file in the response
    return send_file(obj_buffer, mimetype='text/plain', as_attachment=True, download_name=f"mesh.obj")

if __name__ == '__main__':
    app.run(debug=True)
