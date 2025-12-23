terraform {
  required_version = "~> 1.11"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0.0"
    }
  } 
}

provider "google" {
  project     = "francisco-476421"
  region      = "us-west1"
}

module "gcr-play" {
  source = "../../../modules/gcp-cloudrun/"
}

output "registry_uri" {
  value = module.gcr-play.registry_uri
  description = "The created Google Artifact Repository URI"
}

output "secret_id" {
  value = module.gcr-play.secret_id
  description = "The created Secret Manager Secret ID"
}

output "iam_role_email" {
  value = module.gcr-play.role_email
  description = "The created IAM Role Email"
}