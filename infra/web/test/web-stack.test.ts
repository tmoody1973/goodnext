import { App } from "aws-cdk-lib";
import { Match, Template } from "aws-cdk-lib/assertions";
import { GoodNextWebStack } from "../lib/web-stack";

const ARN = "arn:aws:bedrock-agentcore:us-east-1:953791390715:runtime/goodnext_goodnext-j7ndOFF7b3";
const env = { account: "953791390715", region: "us-east-1" };
const plain = Template.fromStack(new GoodNextWebStack(new App(), "Plain", { env, runtimeArn: ARN }));
const secured = Template.fromStack(
  new GoodNextWebStack(new App(), "Secured", { env, runtimeArn: ARN, certificateArn: "arn:aws:acm:us-east-1:953791390715:certificate/abc" }),
);

test("one ARM Fargate task, half a vCPU, one gigabyte, one copy", () => {
  plain.hasResourceProperties("AWS::ECS::TaskDefinition", {
    Cpu: "512",
    Memory: "1024",
    RequiresCompatibilities: ["FARGATE"],
    RuntimePlatform: { CpuArchitecture: "ARM64" },
  });
  plain.hasResourceProperties("AWS::ECS::Service", {
    DesiredCount: 1,
    LaunchType: "FARGATE",
    DeploymentConfiguration: Match.objectLike({ DeploymentCircuitBreaker: { Enable: true, Rollback: true } }),
  });
});

test("the load balancer waits 300 seconds, longer than the slowest plan", () => {
  plain.hasResourceProperties("AWS::ElasticLoadBalancingV2::LoadBalancer", {
    LoadBalancerAttributes: Match.arrayWith([{ Key: "idle_timeout.timeout_seconds", Value: "300" }]),
  });
});

test("health check asks the API every 10 s and drains in 2 min", () => {
  plain.hasResourceProperties("AWS::ElasticLoadBalancingV2::TargetGroup", {
    HealthCheckPath: "/api/health",
    HealthCheckIntervalSeconds: 10,
    HealthyThresholdCount: 2,
    TargetGroupAttributes: Match.arrayWith([{ Key: "deregistration_delay.timeout_seconds", Value: "120" }]),
  });
});

test("the task role may invoke the runtime and read photos with Textract, nothing more", () => {
  plain.hasResourceProperties("AWS::IAM::Policy", {
    PolicyDocument: {
      Statement: Match.arrayWith([
        Match.objectLike({ Action: "bedrock-agentcore:InvokeAgentRuntime", Resource: [ARN, `${ARN}/*`] }),
        Match.objectLike({ Action: "textract:DetectDocumentText", Resource: "*" }),
      ]),
    },
  });
});

test("the container carries the demo clock and the runtime address", () => {
  plain.hasResourceProperties("AWS::ECS::TaskDefinition", {
    ContainerDefinitions: [
      Match.objectLike({
        Environment: Match.arrayWith([
          { Name: "GOODNEXT_ENV", Value: "demo" },
          { Name: "GOODNEXT_DEMO_NOW", Value: "2026-09-10T09:00:00-05:00" },
          { Name: "GOODNEXT_AGENT_RUNTIME_ARN", Value: ARN },
        ]),
        PortMappings: [Match.objectLike({ ContainerPort: 8000 })],
      }),
    ],
  });
});

test("logs are kept one week", () => {
  plain.hasResourceProperties("AWS::Logs::LogGroup", { RetentionInDays: 7 });
});

test("without a certificate: one plain HTTP listener on 80", () => {
  plain.resourceCountIs("AWS::ElasticLoadBalancingV2::Listener", 1);
  plain.hasResourceProperties("AWS::ElasticLoadBalancingV2::Listener", { Port: 80, Protocol: "HTTP" });
});

test("with a certificate: HTTPS on 443 and HTTP redirects", () => {
  secured.resourceCountIs("AWS::ElasticLoadBalancingV2::Listener", 2);
  secured.hasResourceProperties("AWS::ElasticLoadBalancingV2::Listener", { Port: 443, Protocol: "HTTPS" });
  secured.hasResourceProperties("AWS::ElasticLoadBalancingV2::Listener", { Port: 80, DefaultActions: [Match.objectLike({ Type: "redirect" })] });
});
