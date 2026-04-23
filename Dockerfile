# ============================
# 1. Base image (ARM64 native)
# ============================
FROM python:3.10-slim

# ============================
# 2. Install system dependencies
# ============================
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libjpeg-dev \
    libpng-dev \
    libboost-all-dev \
    python3-dev \
    libgtk-3-dev \
    && rm -rf /var/lib/apt/lists/*

# ============================
# 3. Create app directory
# ============================
WORKDIR /app

# ============================
# 4. Copy requirements
# ============================
COPY requirements.txt .

# ============================
# 5. Install Python dependencies
# ============================
RUN pip install --no-cache-dir -r requirements.txt

# ============================
# 6. Copy project files
# ============================
COPY . .

# ============================
# 7. Expose Flask port
# ============================
EXPOSE 5000

# ============================
# 8. Run Flask
# ============================
CMD ["python", "app.py"]