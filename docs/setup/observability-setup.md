## Triton Inference Observability – Setup Guide

System Context :

Environment: Amazon Linux EC2 (GPU node)

Deployment: Triton Inference Server on Kubernetes

Model: ResNet50 (ONNX backend)

Storage: Amazon EFS mounted at /models

Monitoring Stack: Prometheus + Grafana

Perf Analyzer Baseline
Run Triton’s Perf Analyzer to establish throughput and latency metrics:

bash
perf_analyzer -m resnet50 --concurrency-range 32 --batch-size 32
Expected outputs:

Throughput: ~416 inferences/sec

Latency: ~2.4 sec average (queue-heavy)

GPU Compute: ~71 ms per batch

Prometheus Metrics
Key queries to configure in Grafana:

GPU Utilization

promql
DCGM_FI_DEV_GPU_UTIL{gpu="0"}
GPU Memory Usage

promql
DCGM_FI_DEV_FB_USED{gpu="0"}
Throughput

promql
rate(nv_inference_count[1m])
Average Latency

promql
nv_inference_request_duration_us / nv_inference_count
Grafana Panels
GPU utilization (%)

GPU memory usage (MB)

Inference throughput (infer/sec)

Latency breakdown (avg, p50, p95, p99)

Observations
Queue time dominates latency.

GPU compute is efficient once batches are formed.

Metrics confirm end-to-end visibility of inference pipeline.

Future Scope
Multi-model parallelism → Add ResNet18, EfficientNet.

Multi-GPU scaling → Provision additional GPU nodes.

Dynamic batching → Configure preferred_batch_size to reduce queue time.