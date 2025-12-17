
## Debug Tech Spec: Image Pull Error (ImagePullBackOff)

Context:

Cluster: Kubernetes (namespace: inference)

Workload: Triton Inference Server Deployment

Node: ip-10-0-1-149.ec2.internal (GPU node)

Pod: triton-79569cfbbc-m2wcc

Error: ImagePullBackOff due to no space left on device during image unpack.

Symptoms
Pod status: Pending → ImagePullBackOff.

Events show failure to extract image layer:

Code
failed to extract layer ... no space left on device
Init container (amazon/aws-cli:latest) completed successfully.

Triton container failed to pull image:
478253497479.dkr.ecr.us-east-1.amazonaws.com/triton:resnet50.

Root Cause
Large Triton image layers (CUDA libraries, Nsight Compute docs, etc.) exceeded available overlayfs storage.

Node root volume too small (default 20Gi).

Containerd snapshotter unable to write to /var/lib/containerd/io.containerd.snapshotter.v1.overlayfs.

Immediate Remediation
Prune containerd cache to free space:

bash
sudo ctr -n k8s.io images prune
sudo du -sh /var/lib/containerd
Remove unused images/pods:

bash
sudo crictl rmi --prune
Switch to slim Triton image (e.g., nvcr.io/nvidia/tritonserver:23.10-py3-min) to reduce footprint.

Delete and redeploy pod:

bash
kubectl delete pod triton-79569cfbbc -n inference
kubectl get pods -n inference -w
Permanent Resolution
Resize GPU node root volumes to ≥ 100Gi in AWS Launch Template / Terraform.

Optionally, mount a dedicated EBS volume for /var/lib/containerd to isolate container runtime storage.

Bake larger volumes into node bootstrap scripts for reproducibility.

Verification
Pod transitions from ImagePullBackOff → Running.

Logs confirm model load:

bash
kubectl logs deploy/triton -n inference -c triton | grep resnet50
Disk usage check:

bash
df -hT | grep containerd
Lessons Learned
GPU nodes require ≥ 100Gi root volumes for Triton image pulls.

Slim Triton images (py3-min) reduce disk footprint.

Automate containerd cache pruning in node lifecycle hooks.

Document bootstrap steps (nodeadm) for onboarding and reproducibility.


```
Events:
  Type     Reason     Age                  From               Message
  ----     ------     ----                 ----               -------
  Normal   Scheduled  3m9s                 default-scheduler  Successfully assigned inference/triton-79569cfbbc-m2wcc to ip-10-0-1-149.ec2.internal
  Normal   Pulling    3m8s                 kubelet            Pulling image "amazon/aws-cli:latest"
  Normal   Pulled     3m3s                 kubelet            Successfully pulled image "amazon/aws-cli:latest" in 5.419s (5.419s including waiting). Image size: 128976715 bytes.
  Normal   Created    3m3s                 kubelet            Created container: sync-models
  Normal   Started    3m3s                 kubelet            Started container sync-models
  Warning  Failed     61s                  kubelet            Failed to pull image "478253497479.dkr.ecr.us-east-1.amazonaws.com/triton:resnet50": failed to pull and unpack image "478253497479.dkr.ecr.us-east-1.amazonaws.com/triton:resnet50": failed to extract layer (application/vnd.oci.image.layer.v1.tar+gzip sha256:573e602e6564cb45ecb9743e909c510eec7a78e6db1a3a1a7c343c091705bce1) to overlayfs as "extract-871885561-oknc sha256:85b8e878ad28f1bea36973f8a98ff4df41b8cf62db7583f9edce5fca0b9e582f": write /var/lib/containerd/io.containerd.snapshotter.v1.overlayfs/snapshots/360/fs/opt/nvidia/nsight-compute/2023.3.1/docs/pdf/NsightCompute.pdf: no space left on device
  Warning  Failed     61s                  kubelet            Error: ErrImagePull
  Normal   BackOff    60s                  kubelet            Back-off pulling image "478253497479.dkr.ecr.us-east-1.amazonaws.com/triton:resnet50"
  Warning  Failed     60s                  kubelet            Error: ImagePullBackOff
  Normal   Pulling    50s (x2 over 2m59s)  kubelet            Pulling image "478253497479.dkr.ecr.us-east-1.amazonaws.com/triton:resnet50"
```
