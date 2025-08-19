FROM python:3.11-slim

# Set Hugging Face cache directory to a writable location
ENV HF_HOME=/app/hf_cache
RUN mkdir -p /app/hf_cache

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
# Install build-essential (for g++), git, and cmake
RUN apt-get update && apt-get install -y git cmake build-essential && rm -rf /var/lib/apt/lists/*

RUN pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose the port Flask will run on
EXPOSE 5000

# Set environment variable for Flask
ENV FLASK_APP=api.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the Flask app
CMD ["flask", "run"]
