## Troubleshooting – All Issues (EKS / Triton / Monitoring)


This document captures common failure modes and fixes across GPU nodes, EKS modules, Helm deployments, and Triton inference workloads.

🟢 Issue: GPU Feature Discovery (GFD)
Symptom: Pods not scheduling for GPU workloads.
Solution: Deploy/update GFD via Helm.

```

Test Pod:

bash
kubectl run nvidia-test --rm -it --restart=Never \
  --image=nvidia/cuda:13.0-base \
  --overrides='{
    "apiVersion": "v1",
    "spec": {
      "containers": [{
        "name": "nvidia-test",
        "image": "nvidia/cuda:13.0-base",
        "command": ["nvidia-smi"],
        "resources": {
          "limits": {
            "nvidia.com/gpu": 1
          }
        }
      }]
    }
  }'
Node Check:

bash
kubectl describe node <gpu-node> | grep -A10 "Allocated resources:"
→ Should show nvidia.com/gpu 1 1

Root Causes & Fixes
Wrong / Missing GPU Node AMI

Causes GFD errors, driver mismatch, DCGM exporter crash.

Fix: Use AWS Bottlerocket GPU or NVIDIA EKS‑Optimized GPU AMI.

Missing IAM Permissions for Nodegroup

Nodes not joining, CNI/EBS CSI driver failures.

Fix: Attach policies:

AmazonEKSWorkerNodePolicy

AmazonEKS_CNI_Policy

AmazonEC2ContainerRegistryReadOnly

AmazonEBSCSIDriverPolicy

Missing EBS CSI Addon

PVC stuck in Pending.

Fix:

hcl
eks_addons = {
  "aws-ebs-csi-driver" = { most_recent = true }
}
Monitoring Applied Too Soon

CRDs missing, exporters crash.

Fix: Install monitoring only after nodes are healthy.

Cluster Security Group Too Restrictive

Runtime endpoint not listening, GFD blocked.

Fix: Allow internal SG traffic between nodes + control plane.

Not Waiting for Nodegroup Stabilization

GPU labels appear only after GFD runs.

Fix:

bash
kubectl wait --for=condition=ready nodes --all --timeout=300s
🟡 Issue: Prometheus Pod Pending
Causes:

No available CPU/memory.

Missing PVCs.

Node taints not tolerated.

Affinity rules mismatch.

Fixes:

Check node resources.

Override Helm values to use emptyDir:

yaml
prometheus.prometheusSpec.storageSpec.emptyDir.sizeLimit = "2Gi"
🔵 Troubleshooting Log – EC2/EKS/Triton Monitoring
Terraform prompting for var.nodegroup_role_arn

Fix: Fetch ARN via AWS CLI and set in terraform.tfvars or export as TF_VAR_nodegroup_role_arn.

Dependency cycle with aws_auth

Fix: Move aws_auth ConfigMap into separate module, clean state, re‑import.

Helm release error – "cluster unreachable"

Fix: Pass aliased providers (helm.eks, kubernetes.eks) from root into child modules.

Helm release error – "cannot re-use a name"

Fix: Import existing release into Terraform state:

bash
terraform import module.nvidia_plugin.helm_release.nvidia_device_plugin kube-system/nvidia-device-plugin
Prometheus pod stuck in Pending

Fix: Use emptyDir instead of PVC.

Monitoring verification

Confirm Prometheus, Grafana, DCGM exporter pods are running.

Port‑forward services to validate UIs.

Ensure NVIDIA device plugin advertises nvidia.com/gpu.

Test Triton readiness:

bash
curl localhost:8000/v2/health/ready
🔴 Issue: ReplicaSet Not Creating Pods
Condition:

Code
ReplicaFailure   True    FailedCreate
Error creating: pods "triton-..." is forbidden: serviceaccount "triton-sa" not found
Fix: Ensure ServiceAccount exists in namespace:

yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: triton-sa
  namespace: inference
🟣 Issue: CrashLoopBackOff – Models Not Mounting
Symptom: Triton container crashes, /models empty.

Debug PVC Contents:

bash
kubectl run pvc-debug -n inference --rm -it \
  --image=amazon/aws-cli:latest \
  --overrides='{
    "spec": {
      "containers": [{
        "name":"debug",
        "image":"amazon/aws-cli:latest",
        "command":["sh"],
        "stdin":true,
        "tty":true,
        "volumeMounts":[{"mountPath":"/models","name":"model-repo"}]
      }],
      "volumes":[{"name":"model-repo","persistentVolumeClaim":{"claimName":"triton-models-pvc"}}]
    }
  }'
Check PVC Binding:

bash
kubectl get pvc -n inference triton-models-pvc
kubectl describe pvc -n inference triton-models-pvc

```

Notes:

Validate PVC contents before deploying Triton.

Triton exits cleanly if /models is empty or invalid.

Always inspect PVCs with a debug pod instead of exec into crashing container.

✅ Bottom Line
This consolidated triage guide covers:

GPU node setup (GFD, AMIs, IAM, CSI driver).

Monitoring stack readiness (Prometheus, Grafana, DCGM).

Helm deployment issues (service accounts, schema mismatches).

PVC validation for Triton model repository.

Following these steps ensures reproducible fixes and stable GPU inference environments. 

### Triage Matrix : 

```

# Troubleshooting – Quick Reference Matrix

| **Issue**                          | **Symptom**                                                                 | **Cause**                                                                                   | **Fix**                                                                                           |
|------------------------------------|------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| GPU Feature Discovery (GFD)        | Pods not scheduling with `nvidia.com/gpu`                                    | Wrong AMI, missing drivers, GFD not deployed                                                | Use NVIDIA EKS‑Optimized GPU AMI, deploy GFD via Helm, wait for node stabilization                |
| IAM Permissions Missing            | Nodes not joining, CNI/EBS CSI driver failing                                | Nodegroup IAM role missing required policies                                                | Attach `AmazonEKSWorkerNodePolicy`, `AmazonEKS_CNI_Policy`, `AmazonEC2ContainerRegistryReadOnly`, `AmazonEBSCSIDriverPolicy` |
| EBS CSI Addon Missing              | PVC stuck in `Pending`                                                       | EBS CSI driver not installed                                                                | Add `aws-ebs-csi-driver` addon in Terraform/EKS module                                            |
| Monitoring Applied Too Soon        | Prometheus/DCGM exporter CRDs missing, pods crash                            | Monitoring installed before cluster/nodes healthy                                           | Wait until `kubectl get nodes` and system pods are ready before applying monitoring               |
| Cluster Security Group Restrictive | GFD/DCGM exporter cannot talk to kubelet                                     | SG rules block internal traffic                                                             | Allow intra‑cluster SG traffic between nodes and control plane                                    |
| Prometheus Pod Pending             | Pod stuck in `Pending`                                                       | PVC unbound, taints not tolerated, affinity mismatch                                        | Override Helm values to use `emptyDir`, adjust tolerations/affinity                               |
| Terraform var.nodegroup_role_arn   | `terraform plan` prompts for ARN                                             | Variable not set                                                                            | Fetch ARN via AWS CLI and set in `terraform.tfvars` or export as `TF_VAR_nodegroup_role_arn`      |
| Terraform aws_auth cycle           | Error: `Cycle: module.eks.kubernetes_config_map.aws_auth`                    | aws_auth ConfigMap in same module causing dependency cycle                                  | Move aws_auth into separate module, clean state, re‑import                                        |
| Helm cluster unreachable           | `helm_release` error: no configuration provided                              | Providers not passed correctly                                                              | Pass aliased providers (`helm.eks`, `kubernetes.eks`) from root into child modules                |
| Helm release name conflict         | Error: cannot re‑use name                                                    | Release already exists                                                                      | Import existing release into Terraform state                                                      |
| ReplicaSet Failure                 | Deployment shows `ReplicaFailure=True`, pods forbidden due to missing SA     | ServiceAccount not created                                                                  | Add `serviceaccount.yaml` with correct name/namespace                                              |
| CrashLoopBackOff – Models Missing  | Triton container crashes, `/models` empty                                    | PVC not bound or empty                                                                      | Spin up debug pod mounting PVC, inspect `/models`, confirm ResNet50 files exist                   |


``` 