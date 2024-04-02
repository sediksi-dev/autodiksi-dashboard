# app/Dockerfile

FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/sediksi-dev/autodiksi-dashboard.git .

RUN pip3 install -r requirements.txt

EXPOSE $STREAMLIT_PORT

HEALTHCHECK CMD curl --fail http://localhost:$STREAMLIT_PORT/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=$STREAMLIT_PORT", "--server.address=0.0.0.0"]
