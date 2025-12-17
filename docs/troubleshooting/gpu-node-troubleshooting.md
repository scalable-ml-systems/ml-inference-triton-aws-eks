## GPU Node Issues in MLOps Triton Inference 

This document summarizes common challenges when provisioning and running GPU nodes for Triton inference workloads in Kubernetes.

Issues Faced
1. Pod Scheduling Failures
Symptom: Pods stuck in Pending with FailedScheduling.

Cause: Resource requests exceeded node allocatable (CPU, memory, ephemeral storage).

Fix: Reduced ephemeral storage requests to ≤ 18Gi.

2. Disk Pressure Taints
Symptom: node.kubernetes.io/disk-pressure taint blocked scheduling.

Cause: Default 20Gi root volumes; containerd ran out of space unpacking Triton images.

Fix: Increased root volume size to 100Gi via AWS Launch Template.

3. ImagePullBackOff
Symptom: Pod stuck with ImagePullBackOff, error: no space left on device.

Cause: Large Triton image layers exhausted overlayfs storage.

Fixes:

Pruned containerd cache (ctr -n k8s.io images prune).

Switched to py3-min Triton image variant.

Resized root volume for permanent resolution.

4. PVC Binding
Symptom: Pod unable to mount /models.

Cause: PVC misconfiguration or missing EFS mount targets.

Fix: Corrected StorageClass parameters; ensured PVC status = Bound.

5. Node Label/Taint Mismatch
Symptom: Scheduler ignored GPU node.

Cause: Missing or incorrect node labels (accelerator=nvidia).

Fix: Applied consistent labels/taints during nodeadm bootstrap.

Lessons Learned
Align pod resource requests with node allocatable values.

Provision GPU nodes with ≥ 100Gi root volumes.

Document bootstrap steps (nodeadm) for reproducibility.

Use slim Triton images (py3-min) to reduce disk footprint.

Validate PVCs (Bound) before deploying inference workloads.

Next Steps
Bake larger root volumes into Terraform launch templates.

Automate containerd cache pruning in node lifecycle hooks.

