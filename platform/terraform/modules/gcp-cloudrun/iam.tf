locals {
  runtime_roles = [
    "roles/secretmanager.secretAccessor",
    "roles/logging.logWriter",
    "roles/monitoring.metricWriter",
  ]
}

resource "google_service_account" "cloudrun_runtime" {
  project = data.google_client_config.current.project
  account_id   = "otel-python-app-runtime"
  display_name = "Cloud Run runtime SA for otel-python-app"
}

resource "google_project_iam_member" "runtime_roles" {
  for_each = toset(local.runtime_roles)
  project = data.google_client_config.current.project
  role    = each.key
  member  = "serviceAccount:${google_service_account.cloudrun_runtime.email}"
}
