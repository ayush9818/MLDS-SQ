# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /src/app

# Copy the current directory contents into the container at /src/app
# except the .env files
COPY . /src/app/
#RUN find . -name "*.env" -type f -delete

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

ENV CONFIG_PATH /src/app/config/default-config.yaml

RUN chmod +x /src/app/entrypoint.sh

# # Command to run the pipeline or other commands based on the entrypoint script
ENTRYPOINT ["/src/app/entrypoint.sh"]

CMD ["test-app"]
