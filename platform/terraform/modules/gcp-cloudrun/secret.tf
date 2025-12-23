resource "google_secret_manager_secret" "observe_config" {
  project = data.google_client_config.current.project
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
  secret_data = templatefile("${path.module}/templates/observe-agent.yaml", {})
}
