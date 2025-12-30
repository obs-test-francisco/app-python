resource "aws_s3_bucket" "shared_config" {
  bucket_prefix = "${var.ecs.cluster_name}-config-"

  tags = {
    Environment = "dev"
    Application = var.image_name
  }
}

resource "aws_s3_bucket_public_access_block" "shared_config" {
  bucket = aws_s3_bucket.shared_config.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_object" "observe_agent_config" {
  bucket = aws_s3_bucket.shared_config.id
  key    = "observe-agent/observe-agent.yaml"

  etag = filemd5("${path.module}/../../../../tools/observe-agent/observe-agent.ecs.yaml")
  content = templatefile("${path.module}/../../../../tools/observe-agent/observe-agent.ecs.yaml", {
    OBSERVE_URL                      = jsondecode(data.aws_secretsmanager_secret_version.observe.secret_string).OBSERVE_URL
    OBSERVE_TOKEN                    = jsondecode(data.aws_secretsmanager_secret_version.observe.secret_string).OBSERVE_TOKEN
    OBSERVE_OTEL_SERVICE_NAME        = var.image_name
    OBSERVE_OTEL_SERVICE_VERSION     = var.image_version
    OBSERVE_OTEL_SERVICE_ENVIRONMENT = var.environment_name
  })
}
