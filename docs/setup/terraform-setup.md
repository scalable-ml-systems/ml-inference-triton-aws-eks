## Terraform Execution Plan – The Layer Cake

This document defines the correct order of Terraform applies for building a production‑ready EKS cluster with GPU nodes.


``` 
Layered Architecture
Code
 ---------------------------
|        CI/CD Layer         |
 ---------------------------
|       Monitoring           |
 ---------------------------
|    GPU Compute Nodes       |
 ---------------------------
|   Baseline System Nodes    |
 ---------------------------
|      EKS Control Plane     |
 ---------------------------
|   Networking + IAM (VPC)   |
 ---------------------------

 ```
 
Order of Execution
Networking + IAM (Foundation layer)

bash
terraform apply -target=module.vpc
terraform apply -target=module.iam
VPC, subnets, route tables, NAT gateways

Control‑plane IAM roles

Node IAM roles

EKS Control Plane

Create cluster once networking/IAM exist.

Outputs: cluster_endpoint, cluster_ca, cluster_security_group_id, node_role_arn.

No nodes yet — just control plane.

Baseline Nodegroup (System nodes)

Deploy baseline nodes before GPU nodes.

Runs system pods: CoreDNS, VPC CNI, kube‑proxy.

GPU nodes are not meant for system pods.

Confirm cluster health:

bash
kubectl get nodes
kubectl -n kube-system get pods
GPU Nodegroup (Workloads layer)

Apply GPU nodegroup module independently.

At this stage: control plane stable, CNI installed, system nodes healthy.

GPU nodes join normally.

Monitoring (Prometheus, Grafana, DCGM Exporter)

Install only after GPU nodes are healthy.

Guarantees metrics exporters bind correctly.

CI/CD (Last layer)

Depends on IAM OIDC, ECR repository, cluster reachability, Helm charts.

Deploy last to avoid workflow failures.

✅ Bottom Line: Follow this order to avoid bootstrap failures, stuck nodes, and broken monitoring/CI pipelines.