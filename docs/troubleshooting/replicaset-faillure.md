## Kubernetes ReplicaSet Failure – Triton Deployment

### Symptom :

Deployment shows ReplicaFailure=True.

Desired replicas: 1, but 0 pods created.

kubectl get pods -n inference → No resources found.

kubectl logs deploy/triton → timed out waiting for the condition.

Likely Root Causes
PVC Binding Failure

Pod template mounts /models from triton-models-pvc.

If PVC is not Bound, ReplicaSet cannot create pods.

Check:

bash
kubectl get pvc triton-models-pvc -n inference
kubectl describe pvc triton-models-pvc -n inference
Node Selector / Taint Mismatch

Deployment requires accelerator=nvidia node label and toleration nvidia.com/gpu:NoSchedule.

If no GPU node matches, pods remain unscheduled.

Check:

bash
kubectl get nodes --show-labels | grep accelerator=nvidia
kubectl describe node <gpu-node> | grep Taints
Resource Requests Too High

Pod requests: cpu=2, memory=8Gi, nvidia.com/gpu=1.

If node allocatable < requests, scheduler cannot place pod.

Check:

bash
kubectl describe node <gpu-node> | grep Allocatable -A5
Image Pull / Registry Access

Container image: 478253497479.dkr.ecr.us-east-1.amazonaws.com/triton:resnet50.

If ECR auth not configured, pod creation fails silently.

Check events:

bash
kubectl describe rs triton-5fc797b8f8 -n inference | grep -A5 Events
Init Container Failure

Init container sync-models runs amazon/aws-cli:2.16.19.

If it fails (e.g., missing IAM role, PVC not mounted), pod never transitions to Running.

Check:

bash
kubectl describe rs triton-5fc797b8f8 -n inference
Debug Workflow
Check ReplicaSet Events

bash
kubectl describe rs triton-5fc797b8f8 -n inference | sed -n '1,120p'
Verify PVC

bash
kubectl get pvc -n inference
kubectl describe pvc triton-models-pvc -n inference
Confirm GPU Node Availability

bash
kubectl get nodes --show-labels | grep accelerator=nvidia
kubectl get pods -n kube-system -l name=nvidia-device-plugin
Test Image Pull

bash
kubectl run ecr-test --rm -it --restart=Never \
  --image=478253497479.dkr.ecr.us-east-1.amazonaws.com/triton:resnet50 -- bash
Check Init Container Logs

bash
kubectl logs -n inference rs/triton-5fc797b8f8 -c sync-models --tail=100
Quick Fixes
PVC not bound → Fix StorageClass or EFS mount targets.

No GPU node → Label node:

bash
kubectl label node <gpu-node> accelerator=nvidia
Resource mismatch → Lower CPU/memory requests or increase node size.

Image pull error → Ensure ECR IAM role or docker secret configured.

Init container failure → Validate AWS CLI image and PVC mount path.

✅ Bottom Line
Your ReplicaSet is failing because no pods are being created. The most common culprits are PVC not bound, GPU node selector mismatch, or image pull errors. Start by checking ReplicaSet events and PVC status — that usually reveals the blocker immediately.