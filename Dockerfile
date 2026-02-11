# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Define environment variable
ENV MONDAY_API_KEY="eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjYxOTg1NTM0MiwiYWFpIjoxMSwidWlkIjo5OTcxNDYyMiwiaWFkIjoiMjAyNi0wMi0xMVQwNzo0NDowMi4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MzM3NDkyNzAsInJnbiI6ImFwc2UyIn0.xaJ7STOSIKazYotCBJtFjxwqyGPA8xAi6WY0K4QmdhI"
ENV WORK_ORDERS_BOARD_ID="5026565616"
ENV DEALS_BOARD_ID="5026567215"

# Run streamlit when the container launches
CMD ["streamlit", "run", "src/web_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
