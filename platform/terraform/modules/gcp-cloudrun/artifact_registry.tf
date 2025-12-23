resource "google_artifact_registry_repository" "default" {
  location      = "us-west1"
  repository_id = "otel-python-app"
  description   = "OTel Python App"
  format        = "DOCKER"
}