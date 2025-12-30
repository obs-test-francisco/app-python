.PHONY: build clean

GOBIN:=${GOBIN}
GOARCH:=${GOARCH-amd64}
IMAGE_VERSION ?= latest

ECR_BASE_URL := 590183861614.dkr.ecr.us-west-2.amazonaws.com
GCR_BASE_URL := us-west1-docker.pkg.dev/francisco-476421
IMAGE_NAME := otel-python-app
DOCKERHUB := obsfrancisco/${IMAGE_NAME}
ECR := ${ECR_BASE_URL}/docker-hub/obsfrancisco/${IMAGE_NAME}
GCR := ${GCR_BASE_URL}/${IMAGE_NAME}/${IMAGE_NAME}
SOURCE_DIR := ./app

# Default target
all: build tag publish prime

build: 
	cd ${SOURCE_DIR}; \
	docker buildx build . -t obsfrancisco/otel-python-app:${IMAGE_VERSION} \
	--platform linux/amd64,linux/arm64 \
	--target=base \
	--push \
	--load 

prime-ecr:
	docker pull --platform=linux/arm64 ${ECR}:${IMAGE_VERSION} 

tag-gcr:	
	docker tag ${DOCKERHUB}:${IMAGE_VERSION} ${GCR}:latest
	docker tag ${DOCKERHUB}:${IMAGE_VERSION} ${GCR}:${IMAGE_VERSION}

publish-gcr: tag-gcr
	docker push ${GCR}:latest
	docker push ${GCR}:${IMAGE_VERSION} 

publish-dockerhub:
	docker push ${DOCKERHUB}:latest
	docker push ${DOCKERHUB}:${IMAGE_VERSION}

tag: tag-gcr

publish: publish-dockerhub publish-gcr

prime: prime-ecr

run: 
  docker compose up --build

# Help target
help:
	echo "Available targets:"
	echo "  build  - Build the Lambda function"
	echo "  clean  - Clean build artifacts"
	echo "  help   - Show this help message"
