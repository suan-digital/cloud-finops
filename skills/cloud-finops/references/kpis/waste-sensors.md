<!-- Source: finopsfoundation/kpis/waste-sensors (CC BY-SA 4.0) -->

# Waste Sensors

Waste sensors are standardized definitions for potential unrealized savings opportunities.
Tools implement their own visualization and remediation code and use the *id* key to get
descriptions from the FinOps Foundation repository. This standardizes terms across the FinOps domain.

## Waste KPIs

Each waste sensor aggregates a type of unrealized savings opportunities into two types of KPIs:
- **Savings Opportunity** — the actual amount of cost reduction (not the total cost of the unoptimized workload)
- **Waste Percentage** — how much of a workload is in an unoptimized state

When listing multiple waste sensors, sort by largest savings opportunity first.

### Savings Opportunity Example

If total EC2 spend in an account is $1,000 and $200 has low utilization and can be sized
one size smaller, the savings opportunity is $100 (the $200 reduced by half). The waste
percentage is $100 / $1,000 = 10%.

## Waste Goals

A good starting point is to target a Waste Percentage of 5% or less for all workloads.
Goals can be customized by tags (account, application, business unit, etc.).
Performance toward goals should be tracked over time (e.g., monthly Waste Percentage
over 12 months graphed against the target).

## Waste Exceptions

Occasionally workloads may need temporary exceptions from waste sensor tracking
(e.g., Cassandra clusters that cannot easily auto-scale). Exceptions should be
tracked separately with expiration dates.

## Sensor Definitions

| ID | Display Name | Provider | Description | Comment |
|---|---|---|---|---|
| `ws_aws_asg_no_scaling` | AWS ASG No Scaling | aws | Auto scaling group statically configured | No cost avoidance if no other saling conditions are attached to the ASG and the same value for minimum, maximum, and desired capacity is used. |
| `ws_aws_cache_red_family` | AWS Cache Red Family | aws | ElastiCache not in green family | No discounts through prepayment products can be realized as these are only purchased in green zones. |
| `ws_aws_cache_red_region` | AWS Cache Red Region | aws | ElastiCache not in green region | No discounts through prepayment products can be realized as these are only purchased in green zones. |
| `ws_aws_cache_util_low` | AWS Cache Util Low | aws | ElastiCache low utilization | Potential cost avoidance as a smaller size exists and the provisioned resource is underutilized. |
| `ws_aws_ct_duplicate` | AWS CloudTrail Duplicate | aws | More than one CloudTrail trail exists | Potential cost avoidance by eliminating redudant CloudTrail trails as only the first trail is free of charge. |
| `ws_aws_cw_log_no_mgmt_policy` | AWS CloudWatch No Mgmt | aws | CloudWatch logs with no log retention period | Potential cost avoidance by deleting older logs. |
| `ws_aws_ddb_no_scaling` | AWS DDB No Scaling | aws | DynamoDB provisioned read/write capacity not auto scaling | No cost avoidance if the provisioned read/write capacity does not change over time. |
| `ws_aws_ddb_red_region` | AWS DDB Red Region | aws | DynamoDB not in green region | No discounts through prepayment products can be realized as these are only purchased in green zones. |
| `ws_aws_ddb_util_low` | AWS DDB Util Low | aws | DynamoDB provisioned read/write capacity low utilization | Potential cost avoidance as provisioned capacity is underutilized. |
| `ws_aws_ec2_no_asg` | AWS EC2 No Asg | aws | EC2 instance not in auto scaling group | No cost avoidance as the provisioned resource cannot scale based on demand. |
| `ws_aws_ec2_red_family` | AWS EC2 Red Family | aws | EC2 not in green family | No discounts through prepayment products can be realized as these are only purchased in green zones. |
| `ws_aws_ec2_red_network` | AWS EC2 Red Network | aws | EC2 not in green network configuration | No discounts through prepayment products can be realized as these are only purchased in green zones. |
| `ws_aws_ec2_red_os` | AWS EC2 Red OS | aws | EC2 not in green operating system | No discounts through prepayment products can be realized as these are only purchased in green zones. |
| `ws_aws_ec2_red_region` | AWS EC2 Red Region | aws | EC2 not in green region | No discounts through prepayment products can be realized as these are only purchased in green zones. |
| `ws_aws_ec2_red_tenancy` | AWS EC2 Red Tenancy | aws | EC2 not in green tenancy | No discounts through prepayment products can be realized as these are only purchased in green zones. |
| `ws_aws_ec2_util_low` | AWS EC2 Util Low | aws | EC2 low utilization | Potential cost avoidance as a smaller size exists and the provisioned resource is underutilized. |
| `ws_aws_efs_no_mgmt_policy` | AWS EFS No Mgmt | aws | EFS life-cycle management not enabled | Potential cost avoidance by moving EFS files to colder storage offerings. |
| `ws_aws_eip_unattached` | AWS EIP Unattached | aws | EIP not attached to EC2 | Elastic IP address only incurs a cost if they are not attached to an EC2 instance. |
| `ws_aws_emr_red_family` | AWS EMR Red Family | aws | EMR not in green family | No discounts through prepayment products can be realized as these are only purchased in green zones. |
| `ws_aws_emr_red_region` | AWS EMR Red Region | aws | EMR not in green region | No discounts through prepayment products can be realized as these are only purchased in green zones. |
| `ws_aws_es_red_family` | AWS Elasticsearch Red Family | aws | Elasticsearch not in green family | No discounts through prepayment products can be realized as these are only purchased in green zones. |
| `ws_aws_es_red_region` | AWS Elasticsearch Red Region | aws | Elasticsearch not in green region | No discounts through prepayment products can be realized as these are only purchased in green zones. |
| `ws_aws_es_util_low` | AWS Elasticsearch Util Low | aws | Elasticsearch low utilization | Potential cost avoidance as a smaller size exists and the provisioned resource is underutilized. |
| `ws_aws_glue_util_low` | AWS Glue Util Low | aws | Glue Data Processing Units low utilization | Potential cost avoidance as provisioned capacity is underutilized. |
| `ws_aws_iops_util_low` | AWS IOPS Util Low | aws | IOPS low utilization | Potential cost avoidance as provisioned capacity is underutilized. |
| `ws_aws_lambda_util_low` | AWS Lambda Util Low | aws | Lambda provisioned concurrency low utilization | Potential cost avoidance as provisioned capacity is underutilized. |
| `ws_aws_lb_util_low` | AWS LB Util Low | aws | Load Balancer idle | Potential cost avoidance as provisioned capacity is underutilized. |
| `ws_aws_rds_red_family` | AWS RDS Red Family | aws | RDS not in green family | No discounts through prepayment products can be realized as these are only purchased in green zones. |
| `ws_aws_rds_red_region` | AWS RDS Red Region | aws | RDS not in green region | No discounts through prepayment products can be realized as these are only purchased in green zones. |
| `ws_aws_rds_util_low` | AWS RDS Util Low | aws | RDS low utilization | Potential cost avoidance as a smaller size exists and the provisioned resource is underutilized. |
| `ws_aws_rs_red_family` | AWS Redshift Red Family | aws | Redshift not in green family | No discounts through prepayment products can be realized as these are only purchased in green zones. |
| `ws_aws_rs_red_region` | AWS Redshift Red Region | aws | Redshift not in green region | No discounts through prepayment products can be realized as these are only purchased in green zones. |
| `ws_aws_rs_util_low` | AWS Redshift Util Low | aws | Redshift low utilization | Potential cost avoidance as a smaller size exists and the provisioned resource is underutilized. |
| `ws_aws_s3_int_not_active` | AWS S3 Int Not Active | aws | S3 Intelligent Tiering not enabled | Potential cost avoidance by using a managed service that moves infrequently accessed S3 objects to a lower cost storage tier. |
| `ws_aws_s3_no_mgmt_policy` | AWS S3 No Mgmt Policy | aws | S3 life-cycle management not enabled | Potential cost avoidance by moving S3 objects to colder storage offerings. |
| `ws_aws_s3_ver_no_mgmt` | AWS S3 Ver No Mgmt | aws | S3 versioning enabled with no life-cycle policy | Potential cost avoidance by deleting older objects from the version history. |
| `ws_aws_sm_red_family` | AWS SageMaker Red Family | aws | SageMaker not in green family | No discounts through prepayment products can be realized as these are only purchased in green zones. |
| `ws_aws_sm_red_region` | AWS SageMaker Red Region | aws | SageMaker not in green region | No discounts through prepayment products can be realized as these are only purchased in green zones. |
| `ws_aws_sm_util_low` | AWS SageMaker Util Low | aws | SageMaker low utilization | Potential cost avoidance as a smaller size exists and the provisioned resource is underutilized. |
| `ws_aws_snapshot_no_mgmt_policy` | AWS Snapshot No Mgmt | aws | Snapshot life-cycle management not enabled | Potential cost avoidance by life-cycle managing old snapshots. |
| `ws_aws_vpn_no_tunnel` | AWS VPN No Tunnel | aws | VPN has no associated tunnels | Potential cost avoidance as the provisioned VPN has no associated tunnels. |
| `ws_aws_volume_unattached` | AWS Volume Unattached | aws | EBS unattached | Potential cost avoidance by life-cycle managing persistently unattached EBS volumes. |
| `ws_aws_volume_util_low` | AWS Volume Util Low | aws | EBS low utilization | Potential cost avoidance as provisioned capacity is underutilized. |
| `ws_k8s_control_plane_util_low` | K8S Control Plane Util Low | independent | Kubernetes master node low utilization | Potential cost avoidance as provisioned capacity is underutilized. |
| `ws_k8s_dedicated_util_low` | K8S Dedicated Util Low | independent | Kubernetes dedicated nodes low utilization | Potential cost avoidance as provisioned capacity is underutilized. |
| `ws_k8s_node_util_low` | K8S Node Util Low | independent | Kubernetes node low utilization | Potential cost avoidance as provisioned capacity is underutilized. |
| `ws_k8s_pod_util_low` | K8S Pod Util Low | independent | Kubernetes pod low utilization | Potential cost avoidance as provisioned capacity is underutilized. |
| `ws_splunk_no_mgmt_policy` | Splunk No Mgmt | independent | Splunk index with no data retirement and archiving policy | Potential cost avoidance by controlling the size of indexes or the age of data in indexes. |
