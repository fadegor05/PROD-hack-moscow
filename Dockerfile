FROM python:3.12.2-alpine3.19
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE ${BACKEND_PORT}
CMD python -m uvicorn app:create_app --factory --host 0.0.0.0 --port ${BACKEND_PORT}