# 1. Start with a lightweight  Python base image
FROM python:3.12-slim

# 2. Set the working directory
WORKDIR /app

# 3. Configure python and application environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DB_PATH=/data/notes.db

# 4. Install dependencies first
COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy application source code
COPY app ./app/

#6. Create a non-root application user
RUN groupadd --system appgroup && \
    useradd --system --gid appgroup appuser && \
    mkdir -p /data && \
    chown -R appuser:appgroup /app /data

#7. Switch to non-root user
USER appuser

# 8. Document the application port
EXPOSE 5000

# 9. Container health check
HEALTHCHECK --interval=30s --timeout=3s \
    --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health', timeout=2)" || exit 1

#10. Start the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app.app:app"]
