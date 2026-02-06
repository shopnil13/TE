# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies if needed (e.g. for pdfplumber/reportlab)
# pdfplumber/reportlab are mostly pure python but sometimes need build-essentials or libffi-dev
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY extract_pdf.py .
COPY create_dummy_pdf.py .

# Create input and output directories
RUN mkdir -p input output

# Run extract_pdf.py when the container launches
CMD ["python", "extract_pdf.py"]
