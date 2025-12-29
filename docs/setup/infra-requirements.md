🏗️ Core Infrastructure

AWS EKS Cluster – managed Kubernetes control plane

GPU Node Group – EC2 G4/G5 or P-series instances for Triton inference

CPU Node Group – EC2 M5.large/M5.xlarge for regular workloads, CI/CD, and monitoring

VPC + Subnets + Security Groups – isolated networking with secure routing

IAM Roles & Policies – fine-grained access control for nodes and services

Storage:

Amazon EFS – shared persistent storage for models

Amazon S3 – artifact and model repository

⚙️ Kubernetes Layer

Helm – package manager for deploying charts (Triton, monitoring, CI/CD)

Ingress / API Gateway – expose inference endpoints

Istio (minimal service mesh) – secure, observable communication between services

PVCs & StorageClass – persistent volume management for model storage

📦 ML Serving

NVIDIA Triton Inference Server – scalable model deployment

Model Repository – ECR or S3 for storing and versioning models

ONNX / TensorRT / PyTorch models – standardized formats for inference

🔍 Observability & Monitoring

Prometheus – metrics collection (GPU utilization, pod health, latency)

Grafana – dashboards for inference performance and resource usage

Loki / Fluentd – centralized logging

Alertmanager – proactive alerts

DCGM Exporter – NVIDIA GPU metrics exporter for Prometheus

nvidia-smi – GPU diagnostics inside pods/nodes

📂 Storage Plugins

EFS CSI Driver – mount EFS volumes into pods

PersistentVolume / PersistentVolumeClaim – bind workloads to storage

🌐 Networking

Amazon VPC CNI – baseline pod networking in EKS

Calico (optional) – network policies for zero-trust isolation

CNI Metrics Helper – expose CNI metrics to Prometheus

Network Policies – enforce namespace-level traffic rules

🚀 CI/CD & Automation

GitHub Actions – deploy/destroy pipelines (ci/github-actions/deploy-infra.yaml, destroy-infra.yaml)

Terraform – reproducible infrastructure provisioning (EKS, VPC, node groups, storage)

ArgoCD / Flux – GitOps for Kubernetes manifests

Repo Hygiene – .gitignore for sensitive files (*.tfstate, *.tfvars, *.pem, *.onnx)

🔐 Security & Compliance

AWS Secrets Manager / KMS – manage sensitive configs and certificates

RBAC in Kubernetes – role-based access control

Pod Security Policies / OPA Gatekeeper – enforce compliance

Network Policies – restrict pod-to-pod communication

📚 Documentation & Onboarding

README.md – technical value statement and quickstart

Architecture Diagrams – AWS + Kubernetes + Triton flow (EdrawMax/Lucidchart)

Runbooks – GPU provisioning, PVC hygiene, EFS mounting, CI/CD troubleshooting

Onboarding Guides – step-by-step setup for engineers

📝 Provision Order (Essential to Follow)

It is essential to follow this order to ensure reproducibility, teardown hygiene, and correct dependency resolution:

Initialize Terraform

terraform init


Provision Core Infrastructure

VPC, Subnets, Security Groups

IAM Roles & Policies

EKS Cluster

Add Node Groups

GPU node group (Triton inference)

CPU node group (regular workloads)

Install CNI Plugins

Amazon VPC CNI

Calico (optional, for network policies)

CNI Metrics Helper

Install Storage Plugins

EFS CSI Driver

Configure PersistentVolumes and PersistentVolumeClaims

Deploy Observability Stack

Prometheus, Grafana, Loki, Alertmanager

DCGM Exporter for GPU metrics

Deploy NVIDIA Triton Inference Server

Connect to model repository (ECR/S3)

Configure Istio Service Mesh

Secure communication between microservices

Set Up CI/CD Pipelines

GitHub Actions for infra deploy/destroy

ArgoCD / Flux for GitOps

Finalize Documentation

README, diagrams, runbooks, onboarding guides

✅ Summary

This stack ensures:

Compute – GPU + CPU node groups

Storage – EFS CSI + S3

Networking – VPC CNI + Calico

Monitoring – Prometheus, Grafana, DCGM Exporter, nvidia-smi

Automation – Terraform + GitHub Actions + GitOps
