FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl rsync tzdata \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace/Research OS

EXPOSE 8765

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -fsS http://127.0.0.1:8765/api/health >/dev/null || exit 1

CMD ["python3", "research_os.py", "dashboard", "--host", "0.0.0.0", "--port", "8765"]
