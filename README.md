# scalable-triton-inference-eks 

GPU-enabled Triton inference server on Kubernetes/EKS — reproducible, secure, and cost-aware.

This repository provides a production-ready blueprint for serving AI models at scale. 

---

This project delivers a **cloud-native MLOps platform** purpose-built for GPU inference workloads. It combines **NVIDIA Triton Inference Server** with **AWS EKS** to provide: 

-  **High-performance inference** → GPU acceleration for deep learning, LLMs, and computer vision models 
-  **Reproducibility** → Infrastructure-as-code with Terraform and Helm ensures consistent environments across dev, staging, and prod 
-  **Security** → IAM roles via IRSA, scoped permissions, and GitHub OIDC integration for CI/CD trust 
-  **Cost-awareness** → Separate GPU and CPU node groups, teardown hygiene, and lifecycle automation prevent waste 
-  **Observability** → Hooks for Prometheus, Grafana, Loki, and CloudWatch deliver monitoring, logging, and compliance visibility
-  **Scalability & Resilience** → Modular Kubernetes design supports multi-tenant workloads and future service mesh integration

---

## 💼 Business Value

This platform accelerates AI/ML adoption across industries:

- 🧬 **Biotech & Medicine** → Enables faster drug discovery, medical imaging analysis, and precision diagnostics at scale  
- 💳 **Finance & Insurance** → Powers fraud detection, risk modeling, and real‑time customer insights with secure GPU inference  
- 🏨 **Hospitality & Retail** → Delivers personalized recommendations, demand forecasting, and customer experience optimization  
- 🌾 **Agriculture & Energy** → Supports crop yield prediction, resource optimization, and sustainable energy analytics  
- 🏭 **Manufacturing & Logistics** → Improves predictive maintenance, quality control, and supply chain efficiency through AI pipelines  

It solves real-world challenges:

- ❌ Manual GPU provisioning → ✅ Automated, cost-aware node groups  
- ❌ Fragile ML pipelines → ✅ Reproducible, versioned deployments  
- ❌ Security gaps → ✅ IAM-scoped access, IRSA, and GitHub OIDC  
- ❌ No observability → ✅ Hooks for Prometheus, Grafana, and FluentBit  
- ❌ No disaster recovery → ✅ Multi-region scaffolding (planned)

---

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

---

## 🔐 Security & Compliance

- IAM roles scoped via IRSA  
- GitHub OIDC trust for CI/CD  
- Secrets managed via Kubernetes  
- Future: mTLS via Istio service mesh

---

## 📦 Reproducibility & Lifecycle : 

- Infrastructure-as-code via Terraform  
- Helm charts for Triton + observability stack  
- Modular teardown and rebuild workflows  
- Versioned container images via Amazon ECR
- Models hosted in the aws EFS using the kubernetes persistant volume 

---

## 🚀 Outcomes

This isn’t just a cluster — it’s a **launchpad for scalable, a  uditable, cost-efficient AI workloads**.  
Whether you're deploying LLMs, computer vision models, or real-time inference, this platform ensures:

- 🔁 Reproducibility  
- 🔐 Security by default  
- 💰 Cost control  
- 📈 Observability  
- 🧩 Modular onboarding  

