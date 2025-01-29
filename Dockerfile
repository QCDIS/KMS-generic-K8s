FROM python:3.10-alpine

# Create and set the working directory
COPY ./KMS-generic ./KMS-generic
WORKDIR /KMS-generic

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
