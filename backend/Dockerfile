# CPU architecture for this image
# ARG build_for=linux/amd64
# for local mac
ARG build_for=linux/arm64

# Standard base for dbt: https://github.com/dbt-labs/dbt-core/blob/main/docker/Dockerfile
FROM --platform=$build_for python:3.11.2-slim-bullseye as base

# / means the root directory where the Dockerfile is located
COPY / /backend

# Set the working directory (in the container)
WORKDIR /backend

RUN pip install -r requirements.txt

EXPOSE 8112

CMD ["python", "app/backend_app.py"]

