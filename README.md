##  MLOps Inference Platform Using Nvidia Triton Inference Server 

If it isn’t observable, automated, and scalable, it isn’t production-ready. Most AI projects fail at the "last mile" because the infrastructure is an afterthought. This project is a full-stack implementation of a high-concurrency inference ecosystem, modeled after the architectures used by Netflix and Airbnb to serve models at scale.

###  MLOps GPU Inference Platform Stack

- **Inference Server**: NVIDIA Triton (PyTorch, ONNX, TensorRT)
- **Orchestration**: Kubernetes (EKS/GKE)
- **Infrastructure as Code**: Terraform (GPU/CPU node groups, VPC, IAM)
- **Automation**: Python CI/CD pipelines, GitHub Actions
- **Deployment Packaging**: Helm charts (Triton, monitoring, plugins)
- **Storage**: EFS CSI Driver, S3/ECR model repo
- **Networking**: Amazon VPC CNI, Calico (optional), Istio (service mesh)
- **Observability**: Prometheus, Grafana, Loki, DCGM Exporter, `nvidia-smi`
- **Security**: IAM roles, Kubernetes RBAC, Secrets Manager/KMS, Network Policies


### 💼 Business Value

This platform accelerates AI/ML adoption across industries:

- 🧬 **Biotech & Medicine** → Enables faster drug discovery, medical imaging analysis, and precision diagnostics at scale  
- 💳 **Finance & Insurance** → Powers fraud detection, risk modeling, and real‑time customer insights with secure GPU inference  
- 🏨 **Hospitality & Retail** → Delivers personalized recommendations, demand forecasting, and customer experience optimization  
- 🌾 **Agriculture & Energy** → Supports crop yield prediction, resource optimization, and sustainable energy analytics  
- 🏭 **Manufacturing & Logistics** → Improves predictive maintenance, quality control, and supply chain efficiency through AI pipelines  


<img width="800" alt="Triton-Architecture" src="https://github.com/user-attachments/assets/0cfa0d85-4ca5-41d4-9918-b46c08660d81" />



## 🧱 Architecture Overview

| Layer                  | Purpose                                                                 |
|------------------------|-------------------------------------------------------------------------|
| VPC + Subnets          | Isolated, AZ-resilient network for GPU workloads                        |
| IAM + Policies         | Fine-grained access for operators, CI/CD, and IRSA                      |
| EKS Cluster            | Managed Kubernetes control plane with GPU node groups                   |
| Node Groups            | Separate GPU and general-purpose pools for cost control                 |
| ALB Controller (IRSA)  | Ingress with service account–scoped permissions                         |
| Triton Inference       | GPU-enabled pods serving models via gRPC/HTTP                           |
| EFS                    | Shared model repository mounted into Triton pods                        |
| CI/CD                  | GitHub Actions + Terraform + Helm for secure automation                 |
| Observability          | Prometheus, Grafana, Loki, CloudWatch integration                       |



## 🔐 Security & Compliance

- IAM roles scoped via IRSA  
- GitHub OIDC trust for CI/CD  
- Secrets managed via Kubernetes  
- Future: mTLS via Istio service mesh



## 📦 Reproducibility & Lifecycle : 

- Infrastructure-as-code via Terraform  
- Helm charts for Triton + observability stack  
- Modular teardown and rebuild workflows  
- Versioned container images via Amazon ECR
- Models hosted in the aws EFS using the kubernetes persistant volume 



## 🚀 Key Engineering Wins

1. Optimized GPU Utilization
Implemented Dynamic Batching and Instance Groups. This allows the server to group individual inference requests together on the fly, significantly increasing throughput without manual tuning.

2. Multi-Model Concurrency
Configured the ecosystem to serve multiple models (Image Classification & NLP) simultaneously on a single GPU/Node, reducing infrastructure overhead and costs—a critical requirement for Fortune 500 efficiency.

3. SRE-First Observability
Integrated custom Prometheus exporters to track:

   - Inference Latency (p95/p99)

   - Request Queue Time

   - GPU Memory Utilization

---

<img width="600" alt="Grafana-Ytiton-dashboard" src="https://github.com/user-attachments/assets/c8639bd1-4bbb-466e-a1c5-92cf450d6e6c" />



<img width="600" alt="Prometheus-Triton" src="https://github.com/user-attachments/assets/51e758eb-ccc0-4ead-97f9-9387fe3a3724" />


    
<img width="707" height="394" alt="Triton-Tesla-GPU" src="https://github.com/user-attachments/assets/a2417084-add7-4f4a-949d-49ff47979ba0" />

