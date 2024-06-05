FROM python:3.10-slim-buster

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gfortran \
    libatlas-base-dev \
    libjpeg-dev \
    zlib1g-dev \
    libssl-dev \
    libffi-dev \
    default-libmysqlclient-dev \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt /app/

# Install dependencies
RUN pip install --default-timeout=1000 -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV PYTHONUNBUFFERED 1

# Run the Django development server when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]







# Use an official Python runtime as a parent image
# FROM python:3.10

# # Set the working directory in the container
# WORKDIR /app

# # Copy only the requirements file first to leverage Docker cache
# COPY requirements.txt /app/

# RUN apt-get update && apt-get install -y \
#     build-essential \
#     gfortran \
#     libatlas-base-dev \
#     libopenblas-dev \
#     liblapack-dev \
#     && rm -rf /var/lib/apt/lists/*

# # COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --default-timeout=1000 -r requirements.txt

# # Install any needed packages specified in requirements.txt
# RUN pip install -r requirements.txt

# # Copy the current directory contents into the container at /app
# COPY . /app

# # Make port 8000 available to the world outside this container
# EXPOSE 8000

# # Define environment variable
# ENV PYTHONUNBUFFERED 1

# # Run app.py when the container launches
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]



# # First stage: build environment
# FROM python:3.10 AS builder

# # Set the working directory in the builder stage
# WORKDIR /app

# # Upgrade pip to the latest version
# RUN pip install --upgrade pip

# # Install system dependencies for building numpy and other packages
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     gfortran \
#     libatlas-base-dev \
#     libopenblas-dev \
#     liblapack-dev \
#     libssl-dev \
#     libffi-dev \
#     python3-dev \
#     && rm -rf /var/lib/apt/lists/*

# # Copy only the requirements file first to leverage Docker cache
# COPY requirements.txt /app/

# # Install any needed packages specified in requirements.txt in the builder stage
# RUN pip install --default-timeout=1000 -r requirements.txt

# # Second stage: the actual runtime environment
# FROM python:3.10

# # Set the working directory in the final stage
# WORKDIR /app

# # Copy the installed site-packages from the builder stage
# COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# # Copy the current directory contents into the container at /app
# COPY . /app

# # Make port 8000 available to the world outside this container
# EXPOSE 8000

# # Define environment variable
# ENV PYTHONUNBUFFERED 1

# # Run the Django development server when the container launches
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]



# First stage: builder
# FROM python:3.10-slim AS builder

# # Set the working directory in the builder stage
# WORKDIR /app

# # Upgrade pip to the latest version
# RUN pip install --upgrade pip

# # Install system dependencies for building numpy and other packages
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     gfortran \
#     libatlas-base-dev \
#     libopenblas-dev \
#     liblapack-dev \
#     libssl-dev \
#     libffi-dev \
#     python3-dev \
#     default-libmysqlclient-dev \
#     && rm -rf /var/lib/apt/lists/*

# # Copy only the requirements file first to leverage Docker cache
# COPY requirements.txt /app/

# # Install any needed packages specified in requirements.txt in the builder stage
# RUN pip install --default-timeout=1000 -r requirements.txt

# # Second stage: the actual runtime environment
# FROM python:3.10-slim

# # Set the working directory in the final stage
# WORKDIR /app

# # Install runtime dependencies
# RUN apt-get update && apt-get install -y \
#     libatlas-base-dev \
#     libopenblas-dev \
#     liblapack-dev \
#     default-libmysqlclient-dev \
#     && rm -rf /var/lib/apt/lists/*

# # Copy the installed site-packages from the builder stage
# COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# # Copy the current directory contents into the container at /app
# COPY . /app

# # Make port 8000 available to the world outside this container
# EXPOSE 8000

# # Define environment variable
# ENV PYTHONUNBUFFERED 1

# # Run the Django development server when the container launches
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]