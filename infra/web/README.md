# infra/web — public hosting for the demo

One Fargate task behind an Application Load Balancer. The task runs the
single container from the repo-root `Dockerfile`: FastAPI serves `/api/*` and
the static site at `/` (decision 008). The load balancer idle timeout is 300 s
so a food plan (up to ~105 s) is not cut off. The task role allows only
`bedrock-agentcore:InvokeAgentRuntime` and `textract:DetectDocumentText`.

## Deploy

The service pulls its image from the stack's ECR repository, so push the image
before the service can start.

```bash
# 1. Create the ECR repository (first deploy; the service will not stabilize
#    until an image is present).
cd infra/web
npm install
GOODNEXT_AGENT_RUNTIME_ARN='<runtime-arn>' npm run cdk -- deploy

# 2. Build and push the image (from the repo root).
cd ../..
aws ecr get-login-password --region us-east-1 \
  | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker build -t goodnext-web .
docker tag goodnext-web <account>.dkr.ecr.us-east-1.amazonaws.com/goodnext-web:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/goodnext-web:latest

# 3. Roll the service onto the new image.
aws ecs update-service --cluster <cluster> --service <service> --force-new-deployment
```

`RepositoryUri` and `ServiceUrl` are stack outputs. Open `ServiceUrl` in a
browser to reach the demo.

## HTTPS

The task sets `GOODNEXT_COOKIE_SECURE=false` so the session cookie is kept over
plain HTTP until a certificate is attached. When a domain and an ACM
certificate are ready, add an HTTPS listener and drop the override.

## Test

```bash
npm test
```
