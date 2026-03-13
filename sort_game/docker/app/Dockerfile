# ==========================================
# Base Image
# ==========================================

FROM python:3.11-slim


# ==========================================
# Environment
# ==========================================

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app


# ==========================================
# System packages
# ==========================================

RUN apt-get update && apt-get install -y \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*


# ==========================================
# Python dependencies
# ==========================================

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


# ==========================================
# Copy source code
# ==========================================

COPY . .


# ==========================================
# Build C++ sort engine
# ==========================================

RUN g++ -std=c++17 \
    cpp_engine/sort_engine.cpp \
    cpp_engine/algorithms/*.cpp \
    -O2 \
    -o cpp_engine/sort_engine


# ==========================================
# Port
# ==========================================

EXPOSE 5000


# ==========================================
# Run server
# ==========================================

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]