FROM python:3.11.9 

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY agents.py prompts.py ./

RUN mkdir /app/data

CMD ["python", "agents.py"]