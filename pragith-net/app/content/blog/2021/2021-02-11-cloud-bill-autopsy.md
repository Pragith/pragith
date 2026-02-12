---
title: "Cloud Bill Autopsy: How We Saved 30% on Compute"
date: "2021-02-11"
tags: ["Cost Engineering", "AWS", "Kubernetes", "Spot Instances"]
summary: "Our cloud bill grew faster than our user base. We implemented Spot Instances and rigorous tagging to bring unit economics back in line."
status: "published"
---

In January, our cloud bill triggered a CFO alert. We had exceeded our budget by 40%.

The easy answer is "growth." But when we looked at the unit economics—cost per active user—it was trending up, not down. That means we were getting less efficient as we scaled.

We spent two weeks auditing our AWS spend. Here is where the money was bleeding.

## 1. The Development Environment Waste

We found that 25% of our total compute spend was coming from `dev` and `staging` environments running 24/7.

Developers spin up large instances to test a Kafka improvement, then go to sleep. The instance runs all night, all weekend.

**The Fix:** We implemented `kube-downscaler`. It automatically scales all non-production deployments to 0 replicas at 8:00 PM and scales them back up at 8:00 AM. Weekend spend dropped to near zero.

## 2. Spot Instance Adoption

Our batch processing workloads (Airflow workers, Spark jobs) are fault-tolerant. If a node dies, the job retries. Yet, we were running them on On-Demand instances.

**The Fix:** We moved 100% of our batch workloads to Spot Instances. We used `actions-runner-controller` for our CI/CD and configured our EKS node groups to bid on Spot capacity.

We saw a 60-70% reduction in compute costs for these workloads. The trade-off is occasional interruption, but Airflow handles that gracefully.

## 3. The Forgotten EBS Volumes

When you terminate an EC2 instance, the attached EBS volume persists unless you explicitly check "Delete on Termination."

We found 40TB of "orphaned" EBS volumes—disks attached to nothing, just sitting there accruing storage charges. Some were from 2018.

**The Fix:** We wrote a Lambda function that runs daily, identifies unattached volumes older than 7 days, snapshots them (just in case), and deletes them.

## Conclusion

Cloud cost optimization is not a one-time project. It is a hygiene practice.

If you don't have automated tagging policies and lifecycle policies, entropy takes over. The default state of cloud infrastructure is "expensive and unused."
