# OTEL Python Example Application
This repository contains an example Python application instrumented with OpenTelemetry (OTEL) and configured to export telemetry data to Observe. The application is designed to demonstrate how to set up OTEL in a Python environment and deploy it using Docker Compose  and/or AWS ECS Fargate.
 
## Features
* Python application instrumented with OpenTelemetry.
* Exports traces and metrics to Observe via a sidecar container running the Observe Agent.
* Docker Compose setup for local testing.
* Terraform module to deploy the application to AWS ECS Fargate.

## Assumptions/Requirements
* You have an Observe account and have created an ingest token.
* You have AWS credentials configured for Terraform to use.
* You have Docker and Docker Compose installed for local testing.

## Directories
* ./code - Application code and Dockerfiles
* ./code/src - Application code
* ./code/docker - Docker Compose setup for local testing
* ./code/docker/etc/observe-agent/observe-agent.yaml - The Observe Agent configuration file - this is cross-mounted to the observe-agent sidecar container.
* ./code/docker/env-files - Example environment variable files for Docker Compose
* ./terraform/aws/ecs - Terraform module to deploy the application to AWS ECS Fargate

## Required AWS Secrets
The Terraform code expects the following AWS Secrets Manager secrets to be created:
* var.secrets_manager_secrets.dockerhub
  ```json
  {
    "username": "your_dockerhub_username",
    "password": "your_dockerhub_pat"
  }
  ```

* var.secrets_manager_secrets.observe
  ```json
  {
    "OBSERVE_TOKEN": "your_observe_ingest_token",
    "OBSERVE_URL": "https://<tenant_id>.collect.observeinc.com/"
  }
  ```


## Authors
* Francisco Gray - Observe Inc. - francisco.gray@observeinc.com