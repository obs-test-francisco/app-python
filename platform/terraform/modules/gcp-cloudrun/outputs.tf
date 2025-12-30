output "registry_uri" {
  value       = google_artifact_registry_repository.default.registry_uri
  description = "The created Google Artifact Repository URI"
}

output "secret_id" {
  value       = google_secret_manager_secret.observe_config.id
  description = "The created Secret Manager Secret ID"
}

output "role_email" {
  value       = google_service_account.cloudrun_runtime.email
  description = "The created IAM Role Email"
}