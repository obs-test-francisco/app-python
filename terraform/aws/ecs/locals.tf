locals {
  ecr_image_url_base = "590183861614.dkr.ecr.us-west-2.amazonaws.com/docker-hub"
  image_url = {
    app   = "${local.ecr_image_url_base}/${var.image_url}:${var.image_version}"
    agent = "${local.ecr_image_url_base}/observeinc/observe-agent:2.9.1"
    redis = "${local.ecr_image_url_base}/library/redis:6.2"
    mysql = "${local.ecr_image_url_base}/library/mysql:8.0.44"
  }
}
