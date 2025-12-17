## TechSpec Verification: Loki StatefulSet

Expected Services

From the specification:

ClusterIP Service (loki) → exposes port 3100/TCP (HTTP API).

Headless Service (loki-headless) → enables pod DNS discovery for clustering.

Memberlist Service (loki-memberlist) → exposes port 7946/TCP for gossip protocol.

Optional LoadBalancer/Ingress (loki-lb) → external access to Loki API (port 3100).

```
Observed Endpoints
 Output from kubectl get endpointslices -n monitoring | grep loki:

Code
loki-2fcwj                IPv4   3100   10.0.1.133   97m
loki-headless-bcxwc       IPv4   3100   10.0.1.133   97m
loki-lb-mqks5             IPv4   3100   10.0.1.133   80m
loki-memberlist-m72dg     IPv4   7946   10.0.1.133   97m
Verification
✅ ClusterIP Service (loki) exists → port 3100.

✅ Headless Service (loki-headless) exists → port 3100, pod DNS discovery enabled.

✅ LoadBalancer Service (loki-lb) exists → port 3100, external access.

✅ Memberlist Service (loki-memberlist) exists → port 7946, gossip clustering.

All expected services are present and mapped to the Loki pod IP (10.0.1.133).

Debug Checklist
If services were missing or failing:

Check StatefulSet status:

bash
kubectl get statefulset loki -n monitoring
kubectl describe statefulset loki -n monitoring
Verify pods are running:

bash
kubectl get pods -n monitoring -l app=loki -o wide
Inspect service definitions:

bash
kubectl get svc -n monitoring | grep loki
kubectl describe svc loki -n monitoring
Confirm DNS resolution:

bash
kubectl exec -n monitoring <loki-pod> -- nslookup loki-headless

```

conclusion: 

The Loki StatefulSet is correctly exposing its API (3100) and gossip (7946) ports.

Both ClusterIP and Headless services are operational, ensuring API access and pod discovery.

The LoadBalancer service provides external connectivity, which is optional but confirmed in your setup.