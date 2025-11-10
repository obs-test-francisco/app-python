resource "aws_ecs_service" "otel" {
  name                              = var.image_name
  cluster                           = aws_ecs_cluster.default.name
  task_definition                   = aws_ecs_task_definition.otel_combined.arn
  desired_count                     = 1
  launch_type                       = "FARGATE"
  force_delete                      = true
  health_check_grace_period_seconds = 20
  enable_execute_command = true

  network_configuration {
    subnets          = module.vpc.private_subnets
    security_groups  = [aws_security_group.alb.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.default.arn
    container_name   = var.image_name
    container_port   = 8080
  }
}

resource "aws_ecs_task_definition" "otel_combined" {
  family                   = var.image_name
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "4096"
  memory                   = "8192"
  execution_role_arn       = aws_iam_role.task_execution.arn
  task_role_arn            = aws_iam_role.task.arn
  volume {
    name = "shared-config"
  }
  volume {
    name = "shared-logs"
  }
  volume {
    name = "shared-data"
  }

  container_definitions = templatefile("${path.module}/templates/container_definitions.json", {
    init = templatefile("${path.module}/templates/containers/init.json", {
      awslogs_region = data.aws_region.current.region
      awslogs_group  = aws_cloudwatch_log_group.ecs_cluster.name
      image_url = local.image_url.app
      s3_bucket_key = aws_s3_object.observe_agent_config.key
      s3_bucket_name = aws_s3_bucket.shared_config.id
    })
    app = templatefile("${path.module}/templates/containers/app.json", {
      awslogs_region = data.aws_region.current.region
      awslogs_group  = aws_cloudwatch_log_group.ecs_cluster.name
      image_url = local.image_url.app
    })
    agent = templatefile("${path.module}/templates/containers/observe-agent.json", {
      awslogs_region = data.aws_region.current.region
      awslogs_group  = aws_cloudwatch_log_group.ecs_cluster.name
      image_url            = local.image_url.agent
      observe_secrets_arn  = data.aws_secretsmanager_secret.observe.arn
      observe_url_key       = "OBSERVE_URL"
      observe_token_key     = "OBSERVE_TOKEN"
    })
    redis = templatefile("${path.module}/templates/containers/redis.json", {
      awslogs_region = data.aws_region.current.region
      awslogs_group  = aws_cloudwatch_log_group.ecs_cluster.name
      image_url = local.image_url.redis
    })
    mysql = templatefile("${path.module}/templates/containers/mysql.json", {
      awslogs_region = data.aws_region.current.region
      awslogs_group  = aws_cloudwatch_log_group.ecs_cluster.name
      image_url = local.image_url.mysql
    })
  })

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64" # Specify X86_64 architecture
  }
}
