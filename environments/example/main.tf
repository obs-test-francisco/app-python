terraform {
  required_version = "~> 1.0"
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "> 6.0"
    }
  }
}

provider "aws" {
  region = "us-west-2"
}

module "app" {
  source = "../../../terraform/aws/ecs"

  image_url     = "obsfrancisco/otel-python-app"
  image_version = "v0.46.0"
}