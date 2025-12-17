## Find Your EFS Mount Point

```
1. Check PVC → PV Mapping
Confirm that your PVC is bound to a PV:

Code
triton-models-pvc   Bound    triton-models-pv   20Gi   RWX   efs-sc-manual
This indicates that PersistentVolume triton-models-pv is backed by an EFS filesystem.

2. Inspect PV Definition
Run:

bash
kubectl get pv triton-models-pv -o yaml
Look for:

yaml
spec:
  csi:
    driver: efs.csi.aws.com
    volumeHandle: fs-xxxxxxxx
volumeHandle → fs-xxxxxxxx is your EFS FileSystem ID.

3. Find the DNS Name for EFS
Use AWS CLI:

bash
aws efs describe-file-systems --file-system-id fs-xxxxxxxx
aws efs describe-mount-targets --file-system-id fs-xxxxxxxx
The mount target DNS will look like:

Code
fs-xxxxxxxx.efs.us-east-1.amazonaws.com
4. Check EC2 Mounts
On the node:

bash
df -hT | grep efs
mount | grep efs
This shows the actual mount path (commonly /mnt/efs, /efs, or under /var/lib/kubelet/pods/.../volumes/kubernetes.io~csi/...).

5. Next Steps
Once you know the mount path (e.g., /mnt/efs), copy your model repository:

bash
cp -r /home/ubuntu/mlops-k8s-triton-inference/services/triton/models/resnet50 /mnt/efs/triton-models-pv/
Verify inside the pod with a debug container:

bash
kubectl run pvc-debug -n inference --rm -it --image=amazon/aws-cli:latest -- \
  ls /models/resnet50/1
Hygiene Practices
Always confirm the EFS mount path on the node before copying.

Document the PV → PVC → EFS mapping for onboarding engineers.

Keep models versioned and configs at the root of the repository.

Key PV Fields
Example PV spec:

yaml
spec:
  nfs:
    path: /
    server: fs-0e6fc666b970325a9.efs.us-east-1.amazonaws.com
server → DNS name of your EFS (fs-0e6fc666b970325a9.efs.us-east-1.amazonaws.com).

path → / means the root of the EFS filesystem is mounted.

storageClassName → efs-sc-manual confirms manual binding to EFS via NFS. 

```