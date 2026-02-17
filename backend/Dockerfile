# ============================================
# STAGE 1: Base Image
# ============================================
# We use Python 3.11 slim (smaller than full Python image)
# 'slim' = Python + minimal OS dependencies (~150MB vs ~900MB for full)
FROM python:3.11-slim AS base

# Set Python environment variables
# PYTHONUNBUFFERED=1: Print logs immediately (important for Docker)
# PYTHONDONTWRITEBYTECODE=1: Don't create .pyc files (smaller image)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# ============================================
# STAGE 2: Dependencies
# ============================================
# Install system dependencies needed for Python packages
# --no-install-recommends: Only install required packages (keeps image small)
# rm -rf /var/lib/apt/lists/*: Clean up apt cache (reduce image size)
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Build essentials for compiling Python packages
    gcc \
    g++ \
    # For PDF processing (PyMuPDF)
    libmupdf-dev \
    mupdf-tools \
    # For image processing (Pillow)
    libjpeg-dev \
    zlib1g-dev \
    # Tesseract OCR (optional - for debug endpoint)
    tesseract-ocr \
    # Clean up to reduce image size
    && rm -rf /var/lib/apt/lists/*

# ============================================
# STAGE 3: Application Setup
# ============================================
# Set working directory inside container
# All subsequent commands run from /app
WORKDIR /app

# Copy requirements first (Docker layer caching optimization)
# If requirements.txt doesn't change, Docker reuses this layer
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir: Don't cache pip downloads (saves space)
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
# This comes AFTER pip install so code changes don't trigger dependency reinstall
COPY ./app ./app
COPY ./envs ./envs

# Create necessary directories
RUN mkdir -p uploads credentials

# ============================================
# STAGE 4: Runtime Configuration
# ============================================
# Expose port 8000 (FastAPI default)
# This is documentation only - doesn't actually publish the port
EXPOSE 8000

# Set environment variable for production
# This tells config.py to load .env.prod
ENV APP_ENV=prod

# Health check (Docker will restart container if this fails)
# Every 30s, check if the health endpoint responds
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# ============================================
# STAGE 5: Run Command
# ============================================
# CMD: The default command when container starts
# --host 0.0.0.0: Listen on all network interfaces (required for Docker)
# --port 8000: Application port
# --workers 1: Single worker (increase for production based on CPU cores)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]

# ============================================
# BUILD INSTRUCTIONS:
# ============================================
# From backend directory:
#   docker build -t policy-ai-lens-backend .
#
# RUN INSTRUCTIONS:
# From backend directory:
#   docker run -p 8000:8000 \
#     -e GEMINI_API_KEY=your_key \
#     -e GOOGLE_SHEET_ID=your_sheet_id \
#     -v $(pwd)/credentials:/app/credentials \
#     policy-ai-lens-backend
#
# EXPLANATION:
# -p 8000:8000     : Map container port 8000 to host port 8000
# -e               : Pass environment variables
# -v               : Mount local credentials folder into container
# ============================================
