FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip3 install --upgrade pip
RUN python -m pip install --upgrade pip setuptools
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host", "0.0.0.0"]