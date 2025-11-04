variable "image_url" {
  description = "The URL of the Docker image to use for the application"
  type        = string
  default     = "obsfrancisco/otel-python-app"
}

variable "image_version" {
  description = "The version of the Docker image to use for the application"
  type        = string
  default     = "v0.33.0"
}

variable "secrets_manager_secrets" {
  type = map(string)
  default = {
    dockerhub = "ecr-pullthroughcache/dockerhub"
    observe = "provider/observe/francisco-token"
  }
  description = "A map of Secrets Manager secret names for various secrets used by the application"
}


variable "ecs" {
  type = object({
    cluster_name = string
  })
  default = {
    cluster_name = "francisco-dev-cluster"
  }
}