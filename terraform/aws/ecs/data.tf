data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_secretsmanager_secret" "dockerhub" {
  name = var.secrets_manager_secrets.dockerhub
}

data "aws_secretsmanager_secret" "observe" {
  name = var.secrets_manager_secrets.observe
}

data "aws_secretsmanager_secret_version" "observe" {
  secret_id = data.aws_secretsmanager_secret.observe.id
}
