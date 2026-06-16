FROM python:3.11-slim

WORKDIR /app

# Install API dependencies.
COPY services/api/requirements.txt /app/services/api/requirements.txt
RUN pip install --no-cache-dir -r services/api/requirements.txt

# Copy the services and scripts the API loads at runtime.
COPY services /app/services
COPY scripts /app/scripts
COPY agents /app/agents
COPY schemas /app/schemas

# data/ is mounted as a volume in docker-compose.
EXPOSE 8000

CMD ["uvicorn", "services.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
