terraform {
  required_version = "~> 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "> 6.0"
    }
  }
  backend "s3" {
    bucket       = "obsfrancisco-tfstates"
    key          = "ecs-dev/us-west-2/terraform.tfstate"
    region       = "us-west-2"
    use_lockfile = true
  }
}

provider "aws" {
  region = "us-west-2"
}

variable "image_version" {
  type    = string
  default = "v0.50.6"
}

module "app" {
  source = "../../../modules/aws-ecs-fargate/"

  image_url     = "obsfrancisco/otel-python-app"
  image_version = var.image_version
}