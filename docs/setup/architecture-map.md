Architecture Mental Map: AWS, Kubernetes, Triton

High-Level Integration
AWS provides storage and GPU compute.
Kubernetes orchestrates workloads and mounts shared storage.
Triton Inference Server consumes models from EFS and serves inference requests with GPU acceleration.

Textual Mental Map (Checklist + Flow)
1. AWS Layer
Amazon ECR → Hosts Triton container images for deployment.

Amazon EFS → Centralized model repository (resnet50/config.pbtxt, 1/model.onnx).

EC2 GPU Nodes → Back Kubernetes worker nodes with GPU acceleration for inference workloads.

2. Kubernetes Layer
PersistentVolume (PV) → Maps to EFS (fs-xxxx.efs.us-east-1.amazonaws.com:/).

PersistentVolumeClaim (PVC) → Binds PV and mounts into pods at /models.

Helm Chart → Encapsulates Deployment, Service, HPA, and Triton-specific configuration.

3. Pod Layer
Triton Pod → Runs tritonserver container.

PVC Mount → /models inside pod = shared EFS repository.

Init/Sidecar (optional) → Handles model sync or health monitoring.

Service Exposure →

HTTP → :8000

gRPC → :8001

Metrics → :8002

4. Client Layer
Inference Flow → Client requests → Kubernetes Service → Triton Pod → GPU inference execution.

Observability → Prometheus scrapes metrics, Grafana dashboards visualize GPU utilization, latency, and throughput.