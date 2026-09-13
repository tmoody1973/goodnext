#!/usr/bin/env node
import { App } from 'aws-cdk-lib';
import { WebStack } from '../lib/web-stack';

const app = new App();

const agentRuntimeArn = process.env.GOODNEXT_AGENT_RUNTIME_ARN ?? app.node.tryGetContext('agentRuntimeArn');
if (!agentRuntimeArn) {
  throw new Error('Set GOODNEXT_AGENT_RUNTIME_ARN (or -c agentRuntimeArn=...) to the deployed runtime ARN.');
}

new WebStack(app, 'GoodNext-Web', {
  agentRuntimeArn,
  demoNow: process.env.GOODNEXT_DEMO_NOW,
  bedrockRegion: process.env.GOODNEXT_BEDROCK_REGION,
  imageTag: process.env.GOODNEXT_IMAGE_TAG,
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION ?? 'us-east-1',
  },
  description: 'GoodNext public web stack (site + /api/* on one Fargate task behind an ALB)',
});

app.synth();
