#!/usr/bin/env bash
set -euo pipefail

BASE_CONFIG_DIR="${BASE_CONFIG_DIR:-/mnt/shared-config}"
BASE_LOG_DIR="${BASE_LOG_DIR:-/mnt/shared-logs}"

S3_BUCKET_NAME="${S3_BUCKET_NAME:-}"
S3_BUCKET_KEY="${S3_BUCKET_KEY:-}"
S3_OBJECT_URL="s3://${S3_BUCKET_NAME}/${S3_BUCKET_KEY}"

S3_DEST="${BASE_CONFIG_DIR}/"

log() { printf '%s\n' "$*" >&2; }

mkdir -p "${S3_DEST}"
mkdir -p "${BASE_LOG_DIR}/logs"

if [[ -n "${S3_BUCKET_NAME}" && -n "${S3_BUCKET_KEY}" ]]; then
  if command -v aws >/dev/null 2>&1; then
    log "Downloading ${S3_OBJECT_URL} -> ${S3_DEST}/observe-agent.yaml"
    if aws s3 cp "${S3_OBJECT_URL}" "${S3_DEST}/observe-agent.yaml"; then
      log "S3 download succeeded"
      chmod 0644 "${S3_DEST}/observe-agent.yaml" || true
    else
      log "Warning: aws s3 cp failed for ${S3_OBJECT_URL}"
    fi
  else
    log "aws CLI not found; skipping S3 download"
  fi
else
  log "S3_BUCKET_NAME or S3_BUCKET_KEY not set; skipping S3 download"
fi

# Ensure directories are writable by other containers (explicit, limited scope)
chmod -R 0777 "${BASE_LOG_DIR}" "${BASE_CONFIG_DIR}" || true

log "Init complete"
exit 0