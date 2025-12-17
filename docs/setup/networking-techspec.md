## Networking TechSpec: GPU Nodes, VPC, EFS, and NFS

This document summarizes the networking setup and troubleshooting practices for GPU nodes in Amazon EKS clusters, including VPC peering, EFS integration, and NFS mount verification.

1. GPU Nodes in Public Subnet
Launch template must associate a public IP.

Security group must allow SSH from your dev EC2.

Nodes can directly reach the EKS control plane (HTTPS).

2. Private Nodes
Launch in private subnets.

Use a NAT Gateway for outbound internet access.

No public IP → cannot be SSH-ed directly.

3. Terraform Order of Operations
Apply resources in sequence to avoid dependency issues:

Code :

VPC → Subnets → IGW/NAT → Route Tables → EKS → Node Groups

This ensures GPU nodes are created only after subnets and route tables exist.


4. Network Diagram
Code
                 +-----------------------+
                 |      Internet         |
                 +-----------------------+
                          |
                          | 0.0.0.0/0
                          v
                 +-----------------------+
                 |   Internet Gateway    |  <-- module.vpc.aws_internet_gateway.gw
                 +-----------------------+
                          |
          +---------------+-----------------+
          |                                 |
+--------------------+            +--------------------+
|  Public Subnet A   |            |  Private Subnet A  |
|  10.0.1.0/24       |            |  10.0.2.0/24       |
|  map_public_ip=true |            |  map_public_ip=false|
|  RT -> IGW          |            |  RT -> NAT Gateway |
+--------------------+            +--------------------+
          |                                 |
          |                                 |
  +----------------+                +----------------+
  | GPU Node(s)    |                | Private Node(s)|
  | EKS Worker     |                | EKS Worker     |
  | Public IP      |                | No Public IP   |
  +----------------+                +----------------+

                 +-----------------------+
                 | NAT Gateway (Public)  |  <-- module.vpc.aws_nat_gateway.nat_gw_a
                 +-----------------------+
                          |
          +---------------+----------------+
          | Private Subnets outbound only |
          +-------------------------------+


5. VPC Peering Setup
Steps:

Create peering connection between requester and accepter VPCs.

Accept the peering request in the accepter VPC.

Update route tables in both VPCs with peered CIDRs.

Enable enableDnsHostnames and enableDnsSupport in both VPCs.

Troubleshooting:

Verify routes exist in both VPCs.

Confirm SGs/NACLs allow traffic between VPCs.

Use ping or telnet to test connectivity.

6. Amazon EFS Setup
Regional vs One Zone:

Regional EFS → mount targets in every AZ.

One Zone EFS → restricted to a single AZ.

Steps:

Create EFS file system (default: Regional).

Create mount targets in each AZ where nodes run.

Ensure subnet + SG belong to same VPC.

SG rules: inbound TCP/2049 from node SG.

Troubleshooting:

bash
aws efs describe-mount-targets --file-system-id <fs-id> --region us-east-1 --output table
AvailabilityZonesMismatch → One Zone restriction.

SecurityGroupNotFound → SG/subnet mismatch.

7. NFS Mount Verification

Steps on EC2/K8s Node:
```
bash
nslookup <fs-id>.efs.<region>.amazonaws.com
showmount -e <fs-id>.efs.<region>.amazonaws.com
sudo mkdir -p /mnt/efs-test
sudo mount -t nfs4 -o nfsvers=4.1 <fs-id>.efs.<region>.amazonaws.com:/ /mnt/efs-test
df -h | grep efs
mount | grep efs
echo "hello" | sudo tee /mnt/efs-test/verify.txt
cat /mnt/efs-test/verify.txt
```

Troubleshooting:

NXDOMAIN → no mount target in node’s AZ.

Permission denied → SG ingress missing TCP/2049.

Timeout → NACLs or routes blocking traffic.

8. Quick Checklist
[ ] VPC peering accepted and routes updated.

[ ] DNS support enabled in both VPCs.

[ ] Mount targets created in each AZ where nodes run.

[ ] SG inbound rule: TCP/2049 from node SG.

[ ] NACLs allow traffic.

[ ] DNS resolves and manual mount succeeds.




