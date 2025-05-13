# Use the official Playwright image
FROM mcr.microsoft.com/playwright/python:v1.51.0-noble

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run google_maps_reviews.py when the container launches
CMD ["python", "-u", "./main.py"]