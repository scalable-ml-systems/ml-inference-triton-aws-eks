## Kubernetes PV/PVC triage – EFS Mounted but Files Not Visible

Context:

Workload: Triton Inference Server

Storage: Amazon EFS via CSI driver

Symptoms: Pod shows EFS mount, but expected files (e.g., resnet50/) are not visible inside /models repository.

Root Causes & Checks:

```
1. Incorrect Sub-Path or Mount Path
Symptom: EFS is mounted, but directory appears empty.
Cause: Files exist in EFS root, but pod is mounting a different subpath.
Checks:

bash
kubectl exec -it <pod-name> -- sh
ls -la /mnt/efs-test/
ls -la /mnt/efs-test/resnet50
mount | grep efs
df -h | grep efs
Verify from EC2/bastion:

bash
ls -la /mnt/efs/resnet50
Resolution: Ensure files exist at the exact path being mounted.

2. PV/PVC Configuration Mismatch
Symptom: PVC is Bound, but pod mount path doesn’t show expected files.
Cause: PV volumeHandle points to incorrect subpath or root mismatch.
Checks:

yaml
spec:
  csi:
    driver: efs.csi.aws.com
    volumeHandle: fs-12345678:/resnet50   # requires /resnet50 to exist in EFS
    # OR
    volumeHandle: fs-12345678             # mounts EFS root
Resolution:

If using :/subpath, ensure directory exists in EFS root.

If mounting root, copy models directly under / in EFS.

3. EFS CSI Driver SubPath Issue
Symptom: Pod spec uses subPath, but directory not found.
Cause: Kubernetes requires the subPath directory to exist before mounting.
Checks:

yaml
volumeMounts:
  - name: efs-storage
    mountPath: /mnt/efs-test
    subPath: resnet50
Resolution: Pre-create resnet50 directory in EFS before deploying pod.

Debug Workflow
Validate PVC Binding:

bash
kubectl get pvc triton-models-pvc -n inference -o wide
kubectl describe pvc triton-models-pvc -n inference
Inspect PV Definition:

bash
kubectl get pv triton-models-pv -o yaml
Check Pod Mounts:

bash
kubectl describe pod <triton-pod> -n inference | grep -A5 Mounts
Verify Files in Pod:

bash
kubectl exec -n inference <triton-pod> -- ls -la /models/
kubectl exec -n inference <triton-pod> -- ls -la /models/resnet50/
Cross-check EFS Content:

bash
ls -la /mnt/efs/resnet50

```

### Lessons Learned:

Consistency: PV volumeHandle and pod mountPath must align with actual EFS directory structure.

SubPath Hygiene: Directories referenced in subPath must exist in EFS before pod scheduling.

Validation: Always exec into pod and EC2 host to confirm mount paths.

Documentation: Record PV → PVC → EFS mapping for onboarding engineers.

Next Steps:

Standardize PV definitions (avoid ambiguous subpaths).

Automate directory creation in EFS during bootstrap.

Add validation checks in CI/CD to confirm PVC is Bound and directories exist before deployment.