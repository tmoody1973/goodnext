# 012: Host the demo as one container behind one load balancer

Date: September 13, 2026. Status: decided and deployed.

## Decision
The public GoodNext address is one Amazon ECS Fargate container (a small server AWS runs for us without a machine to manage) serving both the static website and the API, behind one Application Load Balancer (the front door that owns the public address and forwards requests) whose idle timeout is raised to 300 seconds. The container calls the deployed agent runtime under an IAM task role (a permission slip attached to the container, so no password or key is stored anywhere).

## Why this came up
Judging needs a public address a stranger can open through October 8. Two facts shape the choice. First, decision 008 says the site and the API share one hostname, because the session cookie is marked "strict same-site" and would be dropped across two addresses. Second, a food plan takes 87 to 105 seconds (HANDOFF.md, measured), so any hop that hangs up at 30, 60, or even 120 seconds breaks the main feature. Getting this wrong means a judge sees "could not reach the service" on the one screen the entry is about.

## Options
1. **ECS Fargate behind an Application Load Balancer** (recommended). One container image holds the site files and the API. Cost: about 12 cloud resources created in one stack, roughly $16 a month for the load balancer plus about $18 a month for the container while it runs, and a certificate needs a domain Tarik owns for HTTPS.
2. **AWS App Runner.** Fewer pieces and HTTPS for free on an AWS-provided hostname. Cost: a hard 120-second request cap, which a 105-second plan can cross on a slow run; no way to raise it.
3. **Lambda with a function URL.** Cheapest at rest and allows 15 minutes. Cost: the API would need response streaming and a different packaging, and the static site a separate host, which breaks decision 008 unless a CDN is added. Not achievable before Monday.
4. **Tarik's Hetzner server with Caddy for HTTPS.** No AWS load balancer cost. Cost: the container would need a long-lived AWS access key on a non-AWS machine, which the handoff rules out ("hosting must run under an IAM role"), and the entry's story is weaker if the app does not run where the agent runs.

## What we chose and why
Option 1, plain HTTP for Monday. Claude recommended it; Tarik approved the resource list and the deploy on September 13 (joint call). Deployed at 13:37 CDT as stack `GoodNext-web`; public address `http://GoodNe-Servi-SOh7w0HGiJhV-1702778700.us-east-1.elb.amazonaws.com`. Two follow-ups the same afternoon: a plain-HTTP listener on port 443 so a browser's https-first attempt fails in milliseconds and falls back (a closed port only drops the packet and the first visit hung), and an ECS circuit breaker so a broken rollout fails in minutes rather than hours.

## What we gave up
Simplicity and a free HTTPS hostname. App Runner would have been fewer resources with HTTPS built in; we traded that for a timeout that fits the slowest request. Without a domain, the site runs on plain HTTP, which the write-up must say. One departure from the handoff: instead of an environment switch that turns the cookie's Secure flag off, the API marks the cookie Secure exactly when the request arrived over HTTPS (the load balancer passes the original scheme along). One rule instead of two settings that must agree. The stack is infrastructure as code (a file describes every resource, so the same command creates or removes them all), but it is a second stack beside the agent's, so there are two things to tear down after judging.

## How we'll know if this was right
A judge opens the public address in a browser, runs Find food today for 53206, and sees a plan after the delayed-status message rather than an error; then uploads the six-month letter and sees the cited result. Both runs recorded under docs/evidence/hosting-live-*. The health route answers from the public address every day through October 8.

## What actually happened
(Tarik fills this in.)
