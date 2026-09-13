// GoodNext public host (decisions 008 and 012): one container behind one load balancer,
// serving the static site at / and the API at /api/*. Nothing stateful lives here.
// Kept apart from agentcore/cdk, which the AgentCore CLI owns and may regenerate.
import * as path from "path";
import { Duration, Stack, type StackProps } from "aws-cdk-lib";
import * as acm from "aws-cdk-lib/aws-certificatemanager";
import * as ec2 from "aws-cdk-lib/aws-ec2";
import * as ecs from "aws-cdk-lib/aws-ecs";
import * as patterns from "aws-cdk-lib/aws-ecs-patterns";
import { Platform } from "aws-cdk-lib/aws-ecr-assets";
import * as iam from "aws-cdk-lib/aws-iam";
import * as logs from "aws-cdk-lib/aws-logs";
import { Construct } from "constructs";

// Judges see September 10, 2026 all day (README, "Demo boundaries").
const DEMO_NOW = "2026-09-10T09:00:00-05:00";
const REPO_ROOT = path.resolve(__dirname, "..", "..", "..");

export interface GoodNextWebStackProps extends StackProps {
  /** The deployed AgentCore runtime (agentcore/.cli/deployed-state.json). */
  runtimeArn: string;
  /** An ACM certificate for a hostname Tarik owns. Absent: plain HTTP, and the API sets a non-Secure cookie. */
  certificateArn?: string;
}

export class GoodNextWebStack extends Stack {
  constructor(scope: Construct, id: string, props: GoodNextWebStackProps) {
    super(scope, id, props);
    const certificate = props.certificateArn ? acm.Certificate.fromCertificateArn(this, "Cert", props.certificateArn) : undefined;

    // The account's default VPC: public subnets only, no NAT gateway to pay for.
    const vpc = ec2.Vpc.fromLookup(this, "Vpc", { isDefault: true });
    const cluster = new ecs.Cluster(this, "Cluster", { vpc, clusterName: "goodnext" });

    const service = new patterns.ApplicationLoadBalancedFargateService(this, "Service", {
      cluster,
      cpu: 512,
      memoryLimitMiB: 1024,
      desiredCount: 1,
      minHealthyPercent: 100,
      // A task that keeps crashing fails the rollout in minutes, not three hours.
      circuitBreaker: { rollback: true },
      assignPublicIp: true,
      // ARM: builds natively on the Mac and runs on Graviton, the cheaper Fargate CPU.
      runtimePlatform: { cpuArchitecture: ecs.CpuArchitecture.ARM64, operatingSystemFamily: ecs.OperatingSystemFamily.LINUX },
      // A food plan takes up to 105 s; the balancer must not hang up first (HANDOFF, Next 1).
      idleTimeout: Duration.seconds(300),
      certificate,
      redirectHTTP: certificate !== undefined,
      taskImageOptions: {
        image: ecs.ContainerImage.fromAsset(REPO_ROOT, { file: "services/api/Dockerfile", platform: Platform.LINUX_ARM64 }),
        containerPort: 8000,
        environment: { GOODNEXT_ENV: "demo", GOODNEXT_DEMO_NOW: DEMO_NOW, GOODNEXT_AGENT_RUNTIME_ARN: props.runtimeArn },
        logDriver: ecs.LogDrivers.awsLogs({
          streamPrefix: "goodnext",
          logGroup: new logs.LogGroup(this, "Logs", { retention: logs.RetentionDays.ONE_WEEK }),
        }),
      },
    });

    // Without HTTPS, let port 443 refuse instantly instead of dropping the packet: modern
    // browsers try https first and fall back to http only after the attempt fails fast.
    if (!certificate) {
      service.loadBalancer.connections.allowFromAnyIpv4(ec2.Port.tcp(443), "Fast refusal so browsers fall back to HTTP");
    }

    // Healthy after 20 s, drained in 2 min: a rollout should not wait longer than the slowest plan.
    service.targetGroup.configureHealthCheck({ path: "/api/health", interval: Duration.seconds(10), healthyThresholdCount: 2 });
    service.targetGroup.setAttribute("deregistration_delay.timeout_seconds", "120");

    // The task may call the agent and read a photo. Nothing else (HANDOFF, Next 1, item 3).
    service.taskDefinition.addToTaskRolePolicy(
      new iam.PolicyStatement({ actions: ["bedrock-agentcore:InvokeAgentRuntime"], resources: [props.runtimeArn, `${props.runtimeArn}/*`] }),
    );
    service.taskDefinition.addToTaskRolePolicy(new iam.PolicyStatement({ actions: ["textract:DetectDocumentText"], resources: ["*"] }));
  }
}
