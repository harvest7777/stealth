### ⚠️ Disclaimer

This project was developed as part of a private take-home assignment. Due to confidentiality, specific requirements and the company name have been omitted.

### Frontend Setup

1. Install dependencies:
   ```bash
   npm install
   npm run dev
> Make sure to replace placeholder values in `.env.example` with your actual credentials and configuration.

### Backend Deployment

This backend is designed to be containerized and deployed using AWS ECS and ECR.

#### Steps (Summary):
1. Build and tag the Docker image.
2. Push it to Amazon ECR.
3. Deploy it via ECS using a task definition and service.

For detailed instructions, refer to the official AWS documentation:
- [Pushing a Docker image to Amazon ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html)
- [Deploying a container on Amazon ECS with Fargate](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-tutorial-fargate.html)

> Make sure to replace placeholder values in `.env.example` with your actual credentials and configuration.

Additionally, copy the environment varialbes into your ECS instance.

### Modal Service Deployment
To deploy this project using [Modal](https://modal.com/), you must first ensure that the following repository is cloned and correctly set up under your own Modal account:

> [PathOn-AI/awesome-lerobot - modal_training](https://github.com/PathOn-AI/awesome-lerobot/tree/main/modal_training)

This repository contains shared functionality required for job execution.

#### After deploying on Modal, you can deploy to AWS.
1. Build and tag the Docker image.
2. Push it to Amazon ECR.
3. Deploy it via ECS using a task definition and service.

For detailed instructions, refer to the official AWS documentation:
- [Pushing a Docker image to Amazon ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html)
- [Deploying a container on Amazon ECS with Fargate](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-tutorial-fargate.html)

Make sure:
- The repo is accessible from your Modal environment
- Any required secrets or credentials are configured in your Modal account

> Make sure to replace placeholder values in `.env.example` with your actual credentials and configuration.

> Additionally, copy the environment varialbes into your ECS instance. For this step, you also need to add MODAL_TOKEN_ID and MODAL_TOKEN_SECRET to your ECS instance. 
> You can view how to retrieve them from the [Modal Documentation](https://modal.com/docs/reference/cli/token)
