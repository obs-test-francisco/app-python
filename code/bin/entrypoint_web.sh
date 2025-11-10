#! /bin/bash

export PATH="/opt/site/.local/bin:$PATH"
BASE_DIR="/opt/site"
CODE_DIR="${BASE_DIR}/code"
ETC_DIR="${BASE_DIR}/etc"

CMD="opentelemetry-instrument \
    --traces_exporter console,otlp \
    --metrics_exporter console,otlp \
    --logs_exporter console,otlp \
    --service_name otel-python-app \
    flask --app app run -h 0.0.0.0 -p ${FLASK_PORT}"

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

echo "Checking if ${LOGS_DIR} dir is writable..."
ls -l /mnt && ls -l "${LOGS_DIR}" && > "${LOGS_DIR}/app-log.json" && ls -l "${LOGS_DIR}"

cd ${CODE_DIR} || exit 1

echo "Running: ${CMD}"
${CMD}

