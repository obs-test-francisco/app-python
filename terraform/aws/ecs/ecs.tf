resource "aws_ecs_cluster" "default" {
  name = var.ecs.cluster_name
}

resource "aws_cloudwatch_log_group" "ecs_cluster" {
  name              = "/ecs/${aws_ecs_cluster.default.name}"
  retention_in_days = 14

  tags = {
    Environment = "dev"
    Application = var.image_name
  }
}