#! /bin/bash

export PATH="/opt/site/.local/bin:$PATH"
CMD="opentelemetry-instrument \
    --traces_exporter console,otlp \
    --metrics_exporter console,otlp \
    --logs_exporter console,otlp  \
    python3 -m debugpy --listen 0.0.0.0:5678 -m flask --app app run -h 0.0.0.0 -p ${FLASK_PORT}"

sigterm() {
  echo "SIGTERM received"
  kill -TERM $PID
  wait $PID
  exit 0
}

sigint() {
  echo "SIGINT received"
  kill -INT $PID
  wait $PID
  exit 0
}

trap sigint SIGINT
trap sigterm SIGTERM

echo "DEBUG: ${CMD}"
${CMD}


