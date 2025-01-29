# FROM python:3.10-slim-bullseye

# RUN echo "you are here"
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# RUN apt update && apt upgrade -y && apt install -y libenchant-2-2

# COPY ./KMS-generic ./KMS-generic
# WORKDIR /KMS-generic

# RUN python -m pip install --upgrade pip
# RUN pip3 install -U pip

# RUN pip3 install -r requirements.txt
# RUN python -m spacy download en_core_web_md

# #CMD ["/bin/sh", "./django_app_setup.sh"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Use the Alpine-based Python image
#FROM python:3.12.4-alpine
FROM python:3.10-alpine

# Create and set the working directory
COPY ./KMS-generic ./KMS-generic
WORKDIR /KMS-generic



#### ENV ####


# Update apk and install required libraries
RUN apk update && \
    apk add --no-cache enchant2-dev g++ gcc libc-dev openblas-dev make musl-dev

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Download Spacy models
RUN python -m spacy download en_core_web_sm && \
    python -m spacy download en_core_web_md

# Expose port 8000 for the Django application
EXPOSE 8000

# Run the Django application on container startup
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
