terraform {
  required_version = "~> 1.11"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0.0"
    }
  }
  backend "gcs" {
    bucket = "obsfrancisco-tfstates"
    prefix = "gcr-dev/us-west1/gcr"
  }
}

provider "google" {
  project = "francisco-476421"
  region  = "us-west1"
}

variable "image_version" {
  type    = string
  default = "v0.50.6"
}

module "gcr-play" {
  source = "../../../../modules/gcp-cloudrun/"
  image_version = var.image_version
}
