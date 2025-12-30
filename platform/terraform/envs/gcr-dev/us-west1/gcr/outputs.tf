output "registry_uri" {
  value       = module.gcr-play.registry_uri
  description = "The created Google Artifact Repository URI"
}

output "secret_id" {
  value       = module.gcr-play.secret_id
  description = "The created Secret Manager Secret ID"
}

output "iam_role_email" {
  value       = module.gcr-play.role_email
  description = "The created IAM Role Email"
}