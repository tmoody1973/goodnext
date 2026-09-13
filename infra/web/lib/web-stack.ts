import { CfnOutput, Duration, RemovalPolicy, Stack, type StackProps } from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as ecr from 'aws-cdk-lib/aws-ecr';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import { ApplicationLoadBalancedFargateService } from 'aws-cdk-lib/aws-ecs-patterns';
import * as iam from 'aws-cdk-lib/aws-iam';
import { Construct } from 'constructs';

/**
 * The public web stack (MOO-793, decision 008): one Fargate task behind an
 * Application Load Balancer, serving the static site and `/api/*` from a single
 * container. The task role is scoped to the two AWS calls the app actually
 * makes: InvokeAgentRuntime (agent_client.py) and DetectDocumentText
 * (notices.py, photo letters).
 */
export interface WebStackProps extends StackProps {
  /** ARN of the deployed AgentCore runtime the API bridges to. */
  agentRuntimeArn: string;
  /** Pinned "today" for the demo clock. Judges see September 10 (handoff). */
  demoNow?: string;
  /** Region of the runtime and Textract. */
  bedrockRegion?: string;
  /** Image tag to pull from the stack's ECR repository. Push before deploy. */
  imageTag?: string;
}

export class WebStack extends Stack {
  constructor(scope: Construct, id: string, props: WebStackProps) {
    super(scope, id, props);

    const {
      agentRuntimeArn,
      demoNow = '2026-09-10T09:00:00-05:00',
      bedrockRegion = 'us-east-1',
      imageTag = 'latest',
    } = props;

    // Public subnets only, no NAT: the task pulls its image and calls AWS over
    // its own public IP, which keeps the demo cheap.
    const vpc = new ec2.Vpc(this, 'Vpc', {
      maxAzs: 2,
      natGateways: 0,
      subnetConfiguration: [{ name: 'public', subnetType: ec2.SubnetType.PUBLIC, cidrMask: 24 }],
    });

    // The single-container image (repo-root Dockerfile). Build and push before
    // deploy; tear-down empties the repository.
    const repository = new ecr.Repository(this, 'Repository', {
      repositoryName: 'goodnext-web',
      imageScanOnPush: true,
      emptyOnDelete: true,
      removalPolicy: RemovalPolicy.DESTROY,
    });

    const cluster = new ecs.Cluster(this, 'Cluster', { vpc });

    const service = new ApplicationLoadBalancedFargateService(this, 'Service', {
      cluster,
      cpu: 512,
      memoryLimitMiB: 1024,
      desiredCount: 1,
      assignPublicIp: true,
      taskSubnets: { subnetType: ec2.SubnetType.PUBLIC },
      publicLoadBalancer: true,
      // A food plan runs up to ~105 s; the ALB default 60 s idle timeout would
      // cut it off, so hold connections open for 300 s.
      idleTimeout: Duration.seconds(300),
      taskImageOptions: {
        image: ecs.ContainerImage.fromEcrRepository(repository, imageTag),
        containerPort: 8000,
        environment: {
          GOODNEXT_ENV: 'demo',
          GOODNEXT_DEMO_NOW: demoNow,
          GOODNEXT_AGENT_RUNTIME_ARN: agentRuntimeArn,
          GOODNEXT_BEDROCK_REGION: bedrockRegion,
          AWS_REGION: bedrockRegion,
          // Plain HTTP until HTTPS lands: a Secure cookie is dropped over HTTP
          // (handoff Next 1, step 5). Remove once a certificate is attached.
          GOODNEXT_COOKIE_SECURE: 'false',
        },
      },
    });

    service.targetGroup.configureHealthCheck({ path: '/api/health' });

    // Least privilege: exactly the two AWS calls in the code.
    service.taskDefinition.taskRole.addToPrincipalPolicy(
      new iam.PolicyStatement({
        actions: ['bedrock-agentcore:InvokeAgentRuntime'],
        resources: [agentRuntimeArn, `${agentRuntimeArn}/*`],
      })
    );
    service.taskDefinition.taskRole.addToPrincipalPolicy(
      new iam.PolicyStatement({
        // DetectDocumentText is not resource-scoped.
        actions: ['textract:DetectDocumentText'],
        resources: ['*'],
      })
    );

    new CfnOutput(this, 'ServiceUrl', {
      description: 'Public URL of the demo',
      value: `http://${service.loadBalancer.loadBalancerDnsName}`,
    });
    new CfnOutput(this, 'RepositoryUri', {
      description: 'Push the container image here before deploy',
      value: repository.repositoryUri,
    });
  }
}
