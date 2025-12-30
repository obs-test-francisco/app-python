resource "google_secret_manager_secret" "observe_config" {
  project   = data.google_client_config.current.project
  secret_id = "observe-config"

  replication {
    user_managed {
      replicas {
        location = "us-west1"
      }
    }
  }
}

resource "google_secret_manager_secret_version" "observe_config_v1" {
  secret      = google_secret_manager_secret.observe_config.id
  secret_data = templatefile("${path.module}/../../../../tools/observe-agent/observe-agent.gcr.yaml", {
    OBSERVE_URL                      = jsondecode(data.google_secret_manager_secret_version.observe.secret_data).OBSERVE_URL
    OBSERVE_TOKEN                    = jsondecode(data.google_secret_manager_secret_version.observe.secret_data).OBSERVE_TOKEN
    OBSERVE_OTEL_SERVICE_NAME        = "otel-python-app"
    OBSERVE_OTEL_SERVICE_VERSION     = var.image_version
    OBSERVE_OTEL_SERVICE_ENVIRONMENT = "gcr-dev"
  })
}