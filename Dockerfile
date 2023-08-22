FROM docker.io/python:3.10-slim


ENV TINI_VERSION="v0.19.0"

ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

RUN pip install --no-cache-dir -U \
    pip \
    setuptools \
    wheel

WORKDIR /app

RUN useradd -m -r user && \
    chown user /app

USER user
ENV PATH=$PATH:/home/user/.local/bin

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


ARG GIT_HASH
ENV GIT_HASH=${GIT_HASH:-dev}

CMD ["/tini", "--", "python", "-m", "streamlit", "run", "streamlitapp.py", "--server.port=8501", "--server.address=0.0.0.0"]