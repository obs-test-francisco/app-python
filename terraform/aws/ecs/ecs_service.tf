resource "aws_ecs_service" "otel" {
  name            = "otel-python-app"
  cluster         = aws_ecs_cluster.default.name
  task_definition = aws_ecs_task_definition.otel_combined.arn
  desired_count   = 1
  launch_type = "FARGATE"
  force_delete = true
  health_check_grace_period_seconds = 20

  network_configuration {
    subnets         = module.vpc.private_subnets
    security_groups = [aws_security_group.alb.id]
    assign_public_ip = false 
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.default.arn
    container_name   = "otel-python-app"
    container_port   = 8080
  }
}

resource "aws_ecs_task_definition" "otel_combined" {
  family                   = "otel-python-app"
  network_mode             = "awsvpc"
  requires_compatibilities  = ["FARGATE"]
  cpu                      = "4096"
  memory                   = "8192"
  execution_role_arn = aws_iam_role.task_execution.arn
  task_role_arn      = aws_iam_role.task.arn
  volume {
    name = "shared-config"
  }
  

  container_definitions = templatefile("${path.module}/templates/container_definition.json", {
    image_url = local.image_url
    dockerhub_secret = data.aws_secretsmanager_secret.dockerhub.arn
    observe_url_secret_arn = "${data.aws_secretsmanager_secret.observe.arn}:OBSERVE_URL"
    observe_token_secret_arn = "${data.aws_secretsmanager_secret.observe.arn}:TOKEN"
  })

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64" # Specify X86_64 architecture
  }
}
