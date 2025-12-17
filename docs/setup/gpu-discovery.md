## GPU Feature Discovery (GFD)

Purpose:  
Runs as a DaemonSet on GPU nodes. Detects GPU hardware/drivers (NVIDIA cards, MIG partitions) and applies node labels (e.g., nvidia.com/gpu.count=1, nvidia.com/mig-1g.5gb=2).

Impact:  
These labels drive Kubernetes scheduling. Without GFD, pods cannot reliably request GPUs.

Key Actions:

Install: Deploy NVIDIA GFD DaemonSet YAML (from nvidia/k8s-device-plugin).

Verify Labels:

bash
kubectl get nodes --show-labels | grep nvidia
Pod Requests:

yaml
resources:
  limits:
    nvidia.com/gpu: 1
Lifecycle: Labels update dynamically if GPUs change (e.g., MIG reconfig).

Dependency: GFD labels nodes; NVIDIA device plugin allocates GPUs.

Checklist:

DaemonSet running:

bash
kubectl get ds -n kube-system | grep gpu-feature-discovery
Labels present:

bash
kubectl describe node | grep nvidia.com
Bottom Line:  
GFD = GPU inventory clerk. It tags nodes with GPU info so the scheduler can place workloads correctly.

NVIDIA Device Plugin MPS Control Daemon
Purpose:  
Manages CUDA Multi-Process Service (MPS) to allow multiple containers to share one GPU efficiently.

Key Points:

MPS: Partitions GPU compute/memory for concurrent workloads.

Deployment: Bundled with NVIDIA device plugin DaemonSet.

Usage: Best for small inference jobs; improves utilization by reducing idle GPU time.

Operation:

Runs as nvidia-device-plugin-mps-control-daemon in kube-system.

Manages nvidia-cuda-mps-server.

Check status:

bash
ps -ef | grep mps
Trade-offs:

No strict isolation; workloads may contend.

Ideal for inference, not heavy training.

Adds complexity to GPU scheduling/debugging.

Bottom Line:  
MPS control daemon = GPU sharing manager. Enables multi-tenant GPU scheduling without wasting full GPUs per pod