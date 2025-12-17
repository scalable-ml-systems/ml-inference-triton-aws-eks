## Nodeadm Bootstrapping on GPU Nodes – TechSpec


### Directory Layout :

```
mlops-k8s-triton-inference/
├── infra/
│   └── terraform/
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       ├── userdata-nodeadm.yaml        # nodeadm MIME payload (launch template bootstrap)
│       └── modules/
│           └── gpu_node_group/
│               ├── main.tf
│               ├── variables.tf
│               ├── outputs.tf
│               ├── launch_template.tf
│               └── userdata-nodeadm.yaml

```

Purpose of userdata-nodeadm.yaml : 

This file defines the Nodeadm bootstrap payload. It ensures GPU nodes are correctly initialized before joining the EKS cluster.

What It Does:

Cluster Join → Uses cluster_name, cluster_endpoint, and cluster_ca passed from Terraform to register node with EKS.

GPU Runtime Setup → Installs NVIDIA driver + container toolkit so pods can request nvidia.com/gpu.

Labels and Taints → Applies accelerator=nvidia label and GPU taint so only GPU workloads land here.

Storage Hygiene → Sets ephemeral storage sizing (≥ 100 Gi) to prevent overlayfs exhaustion.

PVC Clarity → Example shows how to mount EFS PVC at /models for Triton model repository.

Troubleshooting:

Node not joining cluster

Check journalctl -u kubelet for bootstrap errors.

Verify cluster_ca and cluster_endpoint values passed from Terraform.

GPU not visible in pods : 

Confirm NVIDIA driver and container toolkit installed (nvidia-smi works on node).

Ensure NVIDIA device plugin DaemonSet is running in kube-system.

Pods not scheduling on GPU node

Verify node label: kubectl get nodes --show-labels | grep accelerator=nvidia.

Check taints: kubectl describe node <gpu-node> | grep Taints.

Add tolerations to pod spec if taint blocks scheduling.

ImagePullBackOff / Disk Pressure

Confirm root volume ≥ 100 Gi.

Prune containerd cache: sudo ctr -n k8s.io images prune.

PVC not mounting

Check PVC status: kubectl get pvc -n inference.

Ensure EFS mount targets exist in same AZ as node.

Validate volumeHandle path in PV spec matches actual EFS directory.

✅ Bottom Line
The nodeadm-bootstrap-spec is your GPU node initialization contract. It wires together cluster join, GPU runtime, labels/taints, storage sizing, and PVC mounts so Triton inference workloads can land cleanly on GPU nodes. The troubleshooting bullets provide quick triage for common bootstrap failures.