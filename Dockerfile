FROM tiangolo/uvicorn-gunicorn-starlette:python3.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8080
CMD python3 run.py