## Terraform Deployment – Triage Guide

This document maps common mis‑ordering or misconfiguration symptoms to root causes and fixes.

Common Failures
EC2 GPU node stuck in NotReady

Cause: GPU nodegroup applied before baseline nodes.

Fix: Apply baseline nodegroup first; ensure system pods are running.

Kubelet bootstrap failure

Cause: Control plane not reachable (networking/route tables incomplete).

Fix: Verify VPC, subnets, IGW/NAT, and route tables exist before cluster creation.

CNI pods crash / CoreDNS not ready

Cause: GPU nodes used for system pods.

Fix: Deploy baseline nodegroup; taint GPU nodes to prevent system pod scheduling.

SSM/SSH connection fails

Cause: IAM roles or SGs missing.

Fix: Apply IAM module before nodegroups; confirm SG inbound rules.

Monitoring stack fails to install

Cause: Prometheus/Grafana applied before cluster/nodes healthy.

Fix: Wait until kubectl get nodes and kubectl -n kube-system get pods are green.

CI/CD workflows fail

Cause: OIDC provider or ECR not created yet.

Fix: Apply CI/CD layer last; confirm IAM OIDC and ECR repository exist.

Debug Workflow
Check cluster health

bash
kubectl get nodes
kubectl -n kube-system get pods
Inspect Terraform state

bash
terraform state list
Validate networking

bash
aws ec2 describe-route-tables --filters "Name=vpc-id,Values=<vpc-id>"
Confirm IAM roles

bash
aws iam list-roles | grep eks
Check GPU node bootstrap logs

bash
journalctl -u kubelet -n 200 --no-pager
✅ Bottom Line: Most Terraform/EKS failures stem from wrong apply order. Always build foundation → control plane → baseline nodes → GPU nodes → monitoring → CI/CD. Use this triage guide to quickly map symptoms to fixes.