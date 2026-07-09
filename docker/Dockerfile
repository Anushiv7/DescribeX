FROM python:3.11-slim

# Install FFmpeg for video processing
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency files
COPY pyproject.toml .
COPY docker/requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir hatchling

# Copy the engine source
COPY engine/ ./engine/
COPY Readme.md .

# Install the engine package
RUN pip install --no-cache-dir -e .

# Copy the entrypoint
COPY docker/entrypoint.py .

# The hackathon execution model: map /input and /output volumes
# and run the entrypoint script.
ENTRYPOINT ["python", "entrypoint.py"]
