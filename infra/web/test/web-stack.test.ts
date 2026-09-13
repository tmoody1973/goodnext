import * as cdk from 'aws-cdk-lib';
import { Match, Template } from 'aws-cdk-lib/assertions';
import { WebStack } from '../lib/web-stack';

const ARN = 'arn:aws:bedrock-agentcore:us-east-1:123456789012:runtime/goodnext_goodnext-test';

function template(): Template {
  const app = new cdk.App();
  const stack = new WebStack(app, 'TestWebStack', { agentRuntimeArn: ARN });
  return Template.fromStack(stack);
}

test('one Fargate service runs one task', () => {
  const t = template();
  t.resourceCountIs('AWS::ECS::Service', 1);
  t.hasResourceProperties('AWS::ECS::Service', { DesiredCount: 1, LaunchType: 'FARGATE' });
});

test('task is sized 0.5 vCPU / 1 GB', () => {
  template().hasResourceProperties('AWS::ECS::TaskDefinition', { Cpu: '512', Memory: '1024' });
});

test('the image comes from an ECR repository', () => {
  const t = template();
  t.resourceCountIs('AWS::ECR::Repository', 1);
  t.hasResourceProperties('AWS::ECR::Repository', { RepositoryName: 'goodnext-web' });
});

test('the container exposes port 8000 with the demo env', () => {
  template().hasResourceProperties('AWS::ECS::TaskDefinition', {
    ContainerDefinitions: Match.arrayWith([
      Match.objectLike({
        PortMappings: Match.arrayWith([Match.objectLike({ ContainerPort: 8000 })]),
        // Match.arrayWith needs the same relative order as the synthesized array.
        Environment: Match.arrayWith([
          { Name: 'GOODNEXT_ENV', Value: 'demo' },
          { Name: 'GOODNEXT_AGENT_RUNTIME_ARN', Value: ARN },
          { Name: 'GOODNEXT_COOKIE_SECURE', Value: 'false' },
        ]),
      }),
    ]),
  });
});

test('the load balancer idle timeout clears the ~105 s food plan', () => {
  template().hasResourceProperties('AWS::ElasticLoadBalancingV2::LoadBalancer', {
    LoadBalancerAttributes: Match.arrayWith([{ Key: 'idle_timeout.timeout_seconds', Value: '300' }]),
  });
});

test('the health check hits /api/health', () => {
  template().hasResourceProperties('AWS::ElasticLoadBalancingV2::TargetGroup', {
    HealthCheckPath: '/api/health',
  });
});

test('the task role is scoped to the two AWS calls the code makes', () => {
  template().hasResourceProperties('AWS::IAM::Policy', {
    PolicyDocument: {
      Statement: Match.arrayWith([
        Match.objectLike({ Action: 'bedrock-agentcore:InvokeAgentRuntime' }),
        Match.objectLike({ Action: 'textract:DetectDocumentText' }),
      ]),
    },
  });
});

test('the task role holds no wider bedrock-agentcore grant', () => {
  const statements = Object.values(template().findResources('AWS::IAM::Policy')).flatMap(
    policy => policy.Properties.PolicyDocument.Statement as { Action: string | string[] }[]
  );
  const actions = statements.flatMap(s => (Array.isArray(s.Action) ? s.Action : [s.Action]));
  expect(actions).not.toContain('bedrock-agentcore:*');
  expect(actions).not.toContain('bedrock-agentcore:InvokeAgentRuntimeForUser');
});
