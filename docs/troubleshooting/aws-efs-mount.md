## Mounting AWS EFS on EC2 with NFSv4 

This guide explains how to mount an Amazon Elastic File System (EFS) on an EC2 instance using the NFSv4 protocol.

**Prerequisites:**
An EFS file system created in the same VPC as your EC2 instance.

At least one mount target in the same Availability Zone/subnet as your EC2.

Security group rules allowing TCP port 2049 between EC2 and EFS.

**Steps:**
```
1. Verify Mount Target
Ensure the EFS mount target is in the available state:

bash
aws efs describe-mount-targets --file-system-id <fs-id>
2. Install NFS Client
On Ubuntu/Debian:

bash
sudo apt-get update
sudo apt-get install -y nfs-common
On Amazon Linux/RHEL:

bash
sudo yum install -y nfs-utils
3. Create Mount Directory
bash
sudo mkdir -p /mnt/efs
4. Mount EFS Using NFSv4
bash
sudo mount -t nfs4 -o nfsvers=4.1 \
  <fs-id>.efs.<region>.amazonaws.com:/ /mnt/efs
Example:

bash
sudo mount -t nfs4 -o nfsvers=4.1 \
  fs-02441988e987ecd14.efs.us-east-1.amazonaws.com:/ /mnt/efs
5. Verify Mount
bash
df -hT | grep efs
ls -lh /mnt/efs
You should see the EFS mounted as nfs4 with large capacity.

```

Optional: Persist Across Reboots

Add an entry to /etc/fstab:

bash
<fs-id>.efs.<region>.amazonaws.com:/ /mnt/efs nfs4 defaults,_netdev 0 0
Notes
Ensure security groups allow inbound/outbound TCP 2049.

Consider using amazon-efs-utils for TLS encryption and IAM authorization features.

If used for inference with Triton, the directory structure inside /mnt/efs should follow Triton model repository conventions.