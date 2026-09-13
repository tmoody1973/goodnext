#!/usr/bin/env node
// Deploy: cd infra/web && npx cdk diff  (then, on Tarik's go)  npx cdk deploy
// HTTPS:  add  -c certificateArn=arn:aws:acm:...  to both commands.
import * as fs from "fs";
import * as path from "path";
import { App } from "aws-cdk-lib";
import { GoodNextWebStack } from "../lib/web-stack";

// Account, region, and the live runtime ARN come from the agent's own config, never retyped.
const agentcore = path.resolve(__dirname, "..", "..", "..", "agentcore");
const read = (file: string) => JSON.parse(fs.readFileSync(path.join(agentcore, file), "utf8"));
const target = read("aws-targets.json").find((t: { name: string }) => t.name === "default");
const runtimeArn: string = read(".cli/deployed-state.json").targets.default.resources.runtimes.goodnext.runtimeArn;

const app = new App();
new GoodNextWebStack(app, "GoodNext-web", {
  env: { account: target.account, region: target.region },
  runtimeArn,
  certificateArn: app.node.tryGetContext("certificateArn"),
});
