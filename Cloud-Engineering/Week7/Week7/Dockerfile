# Use a base image with Python installed
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files to the working directory
COPY . .

# Expose the Streamlit default port (8501)
EXPOSE 8501

# Set the default command to run when the container starts
CMD ["streamlit", "run", "app.py"]
