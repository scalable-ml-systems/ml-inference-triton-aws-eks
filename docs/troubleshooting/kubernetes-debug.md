## Comprehensive Kubernetes Debug – Triton Server Deployment

This document captures the diagnostic commands used to troubleshoot Triton pods, PVCs, mounts, permissions, GPU device visibility, and node events in Kubernetes.

1. Pod Logs and Exit Reason

List Triton pods:

``` 
bash
kubectl get pods -n inference -l app=triton -o wide
Purpose: Identify pod names, status, node, restarts, and IP.

Show last run logs from a crashed container:

bash
kubectl logs -n inference <pod-name> -c triton --previous --tail=200
Purpose: Retrieve stderr/stdout from the previous run; look for error lines or exit messages.

Show current logs:

bash
kubectl logs -n inference <pod-name> -c triton --tail=200
Purpose: Stream recent logs; useful for running pods or comparison with --previous.

Inspect container lastState:

bash
kubectl get pod -n inference <pod-name> -o jsonpath='{.status.containerStatuses[?(@.name=="triton")].lastState}' | jq .
Purpose: Print exitCode, reason, and message for why the container exited.

2. Pod Description and Events
Describe pod:

bash
kubectl describe pod -n inference <pod-name> | sed -n '1,240p'
Purpose: Inspect pod spec, mounts, env, probes, and Events (scheduling, OOM, probe failures).

List recent namespace events:

bash
kubectl get events -n inference --sort-by='.lastTimestamp' | tail -n 50
Purpose: Review cluster events; check for PVC, device plugin, or scheduling errors.

3. PVC and Volume Checks
Show PVC status:

bash
kubectl get pvc -n inference triton-models-pvc -o wide
Purpose: Confirm PVC is Bound; check storage class, capacity, access modes.

Describe PVC:

bash
kubectl describe pvc -n inference triton-models-pvc | sed -n '1,120p'
Purpose: Inspect PV binding, events, and mount/access errors.

List PVs:

bash
kubectl get pv -o wide
Purpose: Verify PVs, claims, and reclaim policies.

4. Inspect Model Files and Permissions
Create debug pod with PVC mount:

bash
cat <<'EOF' | kubectl apply -n inference -f -; kubectl wait --for=condition=Ready pod/triton-debug -n inference --timeout=60s
apiVersion: v1
kind: Pod
metadata:
  name: triton-debug
spec:
  restartPolicy: Never
  nodeSelector:
    accelerator: nvidia
  containers:
  - name: debug
    image: alpine
    command: ["/bin/sh","-c","sleep 1d"]
    volumeMounts:
    - name: model-repo
      mountPath: /models
  volumes:
  - name: model-repo
    persistentVolumeClaim:
      claimName: triton-models-pvc
EOF
Purpose: Mount PVC into a debug pod for safe inspection.

List files in model directory:

bash
kubectl exec -n inference -it triton-debug -- sh -c "ls -la /models; find /models -maxdepth 3 -type d -print | head -n 50"
Purpose: Verify directory structure and presence of config.pbtxt.

Check ownership and permissions:

bash
kubectl exec -n inference -it triton-debug -- sh -c "stat -c '%U:%G %a %n' /models /models/* 2>/dev/null || true; getfacl /models 2>/dev/null || true"
Purpose: Confirm Triton runtime user can read/traverse directories.

5. GPU Device and Driver Checks
Check NVIDIA device nodes:

bash
kubectl exec -n inference -it triton-debug -- sh -c "ls -l /dev | grep nvidia || true"
Purpose: Verify /dev/nvidia* devices are visible in pod.

Check for nvidia-smi:

bash
kubectl exec -n inference -it triton-debug -- sh -c "which nvidia-smi || ls -l /usr/bin/nvidia-smi /usr/local/bin/nvidia-smi 2>/dev/null || true"
Purpose: Confirm nvidia-smi binary presence.

Check device plugin DaemonSet:

bash
kubectl get ds -n kube-system -o wide | grep -i nvidia || kubectl get pods -n kube-system -l 'app in (nvidia-device-plugin)' -o wide
Purpose: Ensure NVIDIA device plugin is running.

View device plugin logs:

bash
kubectl logs -n kube-system daemonset/nvidia-device-plugin-daemonset --tail=200 || kubectl logs -n kube-system -l name=nvidia-device-plugin --tail=200
Purpose: Inspect plugin registration/device mount errors.

6. Binary, Library, and Manual Triton Run Checks
Locate tritonserver binary:

bash
kubectl run -n inference triton-run --rm -it --restart=Never --image=478253497479.dkr.ecr.us-east-1.amazonaws.com/triton:24.01-py3 -- sh -c "which tritonserver || ls -l /opt/tritonserver /opt/tritonserver/bin || true"
Run Triton manually with verbose logs:

bash
kubectl run -n inference triton-run --rm -it --restart=Never --image=478253497479.dkr.ecr.us-east-1.amazonaws.com/triton:24.01-py3 -- sh -c "/opt/tritonserver/bin/tritonserver --model-repository=/models --log-verbose=1 2>&1 | sed -n '1,200p'"
Check shared library dependencies:

bash
kubectl run -n inference triton-run --rm -it --restart=Never --image=478253497479.dkr.ecr.us-east-1.amazonaws.com/triton:24.01-py3 -- sh -c "ldd /opt/tritonserver/bin/tritonserver 2>/dev/null | sed -n '1,200p' || true"
7. Node and Kubelet Diagnostics
Describe GPU node:

bash
kubectl describe node <gpu-node-name> | sed -n '1,240p'
Purpose: Inspect allocatable resources, labels, taints, and events.

View kubelet logs (node access required):

bash
sudo journalctl -u kubelet -n 200 --no-pager
Purpose: Check for device plugin failures, cgroup denials, or OOM events.

8. Cleanup and Helper Commands
Delete debug pod:

bash
kubectl delete pod -n inference triton-debug --ignore-not-found
Scale Triton deployment:

bash
kubectl scale deploy triton -n inference --replicas=1
Restart deployment:

bash
kubectl rollout restart deploy triton -n inference

```

Usage Flow: 

Start with pod logs and lastState to capture exit reason.

If inconclusive, create triton-debug pod to inspect /models and GPU device visibility.

If models exist but Triton exits, run manual tritonserver in a throwaway container to reveal library/CUDA errors.

If scheduling issues persist, inspect node capacity, device plugin, and PVC binding.