## NVIDIA-SMI – TechSpec

### Purpose :

nvidia-smi (NVIDIA System Management Interface) is a command-line utility that provides visibility into GPU devices, drivers, and CUDA runtime on a node. It is bundled with the NVIDIA driver and CUDA toolkit.

What It Does:

Driver & CUDA Info → Reports installed NVIDIA driver version and CUDA runtime version.

GPU Inventory → Lists all GPUs on the node (name, bus ID, persistence mode).

Health Metrics → Shows temperature, power usage, performance state, and ECC error status.

Memory Utilization → Displays total GPU memory and current usage.

Process Table → Lists processes using the GPU, including PID, type, and memory consumption.

MIG Awareness → Reports Multi-Instance GPU (MIG) partitions if enabled.

Typical Usage

Run inside a pod or directly on a node to confirm GPU visibility:

``` 
bash
kubectl run nvidia-test --rm -it --restart=Never \
  --image=nvidia/cuda:13.0.1-base-ubuntu22.04 -- nvidia-smi
Expected output includes:

Driver version (e.g., 580.105.08).

CUDA version (e.g., 13.0).

GPU details (e.g., Tesla T4).

Memory usage (e.g., 0MiB / 15360MiB).

Process table (empty if no workloads are running).

``` 
Why It Matters
Confirms that GPU drivers and CUDA runtime are correctly installed.

Validates that Kubernetes pods can access /dev/nvidia* devices.

Provides a quick health check for GPU nodes before deploying inference workloads.

Essential for debugging GPU scheduling, resource allocation, and runtime errors.

✅ Bottom Line:  
nvidia-smi is the first-line diagnostic tool for GPU nodes. If it runs successfully inside a pod, you know the NVIDIA driver, CUDA runtime, and device plugin are working correctly.

```
dev-ec2-->kubectl run nvidia-test-2 --rm -it --restart=Never   --image=nvidia/cuda:13.0.1-base-ubuntu22.04   -- nvidia-smi
Wed Dec 10 03:56:00 2025       
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 580.105.08             Driver Version: 580.105.08     CUDA Version: 13.0     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  Tesla T4                       On  |   00000000:00:1E.0 Off |                    0 |
| N/A   24C    P8             16W /   70W |       0MiB /  15360MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|  No running processes found                                                             |
+-----------------------------------------------------------------------------------------+
pod "nvidia-test-2" deleted from default namespace

```
