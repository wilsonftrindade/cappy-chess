FROM python:3.11.9
WORKDIR /backend

RUN apt-get update && apt-get install -y \
    --no-install-recommends stockfish \
    && rm -rf /var/lib/apt/lists/* 

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV STOCKFISH_PATH=/usr/games/stockfish

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]