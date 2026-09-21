FROM python:3.12-slim

WORKDIR /app

# JRE/JDK is intentionally installed in v1 because ANTLR generation and the
# future Run milestone need Java. Optimize to a multi-stage image later.
RUN apt-get update \
    && apt-get install -y --no-install-recommends default-jdk curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Generate ANTLR Python sources only when src/grammar/OPLang.g4 has been migrated.
RUN if [ -f src/grammar/OPLang.g4 ]; then bash scripts/build_antlr.sh; fi

ENV PYTHONPATH=/app
ENV PORT=10000

CMD ["sh", "-c", "uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-10000}"]
