## Triton Inference Observability – Triage Guide

### Common Issues & Fixes

Grafana panel empty

Check Prometheus scrape config for Triton metrics endpoint (:8002/metrics).

Verify ServiceMonitor labels match Triton service.

GPU utilization flat at 0%

Confirm NVIDIA device plugin DaemonSet is running in kube-system.

Run kubectl exec -it <pod> -- nvidia-smi to verify GPU visibility.

Memory usage not reported

Ensure DCGM exporter is deployed and scraping GPU metrics.

Check kubectl logs dcgm-exporter -n monitoring.

Perf Analyzer throughput mismatch

Verify batch size and concurrency flags match Grafana queries.

Check if pods are resource-constrained (CPU/memory throttling).

Latency panels missing

Confirm Triton metrics are enabled (--metrics-port=8002).

Inspect logs: kubectl logs deploy/triton -n inference | grep metrics.

Prometheus scrape errors

Run kubectl get servicemonitors -n monitoring to confirm targets.

Check kubectl logs prometheus-k8s-0 -n monitoring for scrape failures.

Quick Checklist
[ ] Triton metrics endpoint reachable (curl <pod-ip>:8002/metrics).

[ ] Prometheus ServiceMonitor configured with correct labels.

[ ] DCGM exporter running and reporting GPU stats.

[ ] Grafana datasource points to Prometheus.

[ ] Perf Analyzer results align with Grafana panels.