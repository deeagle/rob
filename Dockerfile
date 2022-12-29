FROM python:slim-bullseye

LABEL org.opencontainers.image.authors="Martin Kock <code@deeagle.de>" \
      org.opencontainers.image.url="https://github.com/deeagle/rob" \
      org.opencontainers.image.licenses="GPL3" \
      org.opencontainers.image.title="ROBpy" \
      org.opencontainers.image.description="Container for ROBpy instances." \
      org.opencontainers.image.vendor="deeagle.de"

RUN apt-get -y update \
  && apt-get -yq upgrade \
  && apt-get install --no-install-recommends --assume-yes \
    vim \
  && rm -Rf /var/lib/apt/lists/*

RUN mkdir -p /app/rob

COPY ["src/main.py", "/app/rob/main.py"]
COPY ["src/config.dist.yml", "/app/rob/config.dist.yml"]
COPY ["CHANGELOG.md", "/app/rob/CHANGELOG.md"]
COPY ["README.md", "/app/rob/README.md"]

COPY ["requirements.txt", "/app/rob/requirements.txt"]

RUN pip install --no-cache-dir -r /app/rob/requirements.txt

WORKDIR /app/rob

CMD ["/bin/bash"]
