## Runbook Checklist: Triton Deployment Prep 


**Pre‑Deployment To‑Do List**
```
1. Verify EFS Setup
[ ] Confirm PV → PVC binding:

bash
kubectl get pv,pvc -n inference
[ ] Note EFS DNS (e.g., fs-xxxx.efs.us-east-1.amazonaws.com).

[ ] Mount EFS locally on GPU node:

bash
sudo mkdir -p /mnt/efs
sudo mount -t nfs4 -o nfsvers=4.1 fs-xxxx.efs.us-east-1.amazonaws.com:/ /mnt/efs
2. Prepare Model Repository
[ ] Create directory structure:

Code
resnet50/
├── config.pbtxt
└── 1/
    └── model.onnx
[ ] Validate config.pbtxt matches ONNX input/output names.

3. Copy Models into EFS
[ ] Copy repo into PVC path:

bash
cp -r /home/ubuntu/mlops-k8s-triton-inference/services/triton/models/resnet50 /mnt/efs/triton-models-pv/
[ ] Verify inside EFS:

bash
ls -lh /mnt/efs/triton-models-pv/resnet50/1/
4. Deploy Triton
[ ] Run Helm:

bash
helm upgrade --install triton ./helm -n inference -f helm/values.yaml
[ ] Watch pods:

bash
kubectl get pods -n inference -w
5. Validate Model Load
[ ] Check logs:

bash
kubectl logs -n inference deploy/triton -c triton | grep resnet50
[ ] Confirm model resnet50 loaded successfully.

6. Smoke Test Inference
[ ] Health check:

bash
curl http://<triton-service>:8000/v2/health/ready
[ ] Send inference request (JSON input → classification output).
```