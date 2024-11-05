FROM python:3.9-slim

# Set a working directory inside the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . /app

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port Flask is running on
EXPOSE 5000
# Run the Flask app
CMD ["flask", "run"]
