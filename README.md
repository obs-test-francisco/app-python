# OTEL Python Application Example with Observe
This repository contains an example Python application instrumented with OpenTelemetry (OTEL) and configured to export telemetry, metrics, and log data to Observe. 

The application is designed to demonstrate how to set up OTEL in a Python environment and deploy it using Docker Compose and/or AWS ECS Fargate or Google Cloud Run.
 
## Features
* Python/Redis/MySQL application instrumented with OpenTelemetry.
* Exports traces, metrics, and logs to Observe via a sidecar container running the [Observe Agent](https://github.com/observeinc/observe-agent).
* Docker Compose setup for local testing.
* Terraform module to deploy the application to AWS ECS/Fargate.
* Terraform module to deploy the application to Google Cloud Run.

## Assumptions/Requirements
* You have Docker and Docker Compose installed for local testing.
* You have an Observe account and have created an ingest token.

## AWS Assumptions/Requirements
* You have AWS credentials configured for Terraform to use.

## Google Cloud Assumptions/Requirements
* You have Google Cloud credentials configured for Terraform to use.
* You have enabled the Cloud Run and Secret Manager APIs in your Google Cloud project.

## Directories
* ./app - Application code and Dockerfiles
* ./app/bin - Application startup scripts
* ./app/src - Application code
* ./tools/docker/env-files - Example environment variable files for Docker Compose
* ./tools/observe-agent/observe-agent.yaml - The Observe Agent configuration file - this is cross-mounted to the observe-agent sidecar container.
* ./platform/cloudrun/ - Google Cloud Run deployment files
* ./platform/knative/ - Kubernetes/Knative deployment files
* ./platform/terraform/aws/ecs - Terraform module to deploy the application to AWS ECS Fargate
* ./platform/terraform/modules/gcp-cloudrun - Terraform module to deploy the application to Google Cloud Run
* ./platform/terraform/envs - Terraform environment configurations

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