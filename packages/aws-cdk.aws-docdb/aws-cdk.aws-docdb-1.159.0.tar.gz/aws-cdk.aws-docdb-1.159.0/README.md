# Amazon DocumentDB Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

## Starting a Clustered Database

To set up a clustered DocumentDB database, define a `DatabaseCluster`. You must
always launch a database in a VPC. Use the `vpcSubnets` attribute to control whether
your instances will be launched privately or publicly:

```python
# vpc: ec2.Vpc

cluster = docdb.DatabaseCluster(self, "Database",
    master_user=docdb.Login(
        username="myuser",  # NOTE: 'admin' is reserved by DocumentDB
        exclude_characters="\"@/:",  # optional, defaults to the set "\"@/" and is also used for eventually created rotations
        secret_name="/myapp/mydocdb/masteruser"
    ),
    instance_type=ec2.InstanceType.of(ec2.InstanceClass.R5, ec2.InstanceSize.LARGE),
    vpc_subnets=ec2.SubnetSelection(
        subnet_type=ec2.SubnetType.PUBLIC
    ),
    vpc=vpc
)
```

By default, the master password will be generated and stored in AWS Secrets Manager with auto-generated description.

Your cluster will be empty by default.

## Connecting

To control who can access the cluster, use the `.connections` attribute. DocumentDB databases have a default port, so
you don't need to specify the port:

```python
# cluster: docdb.DatabaseCluster

cluster.connections.allow_default_port_from_any_ipv4("Open to the world")
```

The endpoints to access your database cluster will be available as the `.clusterEndpoint` and `.clusterReadEndpoint`
attributes:

```python
# cluster: docdb.DatabaseCluster

write_address = cluster.cluster_endpoint.socket_address
```

If you have existing security groups you would like to add to the cluster, use the `addSecurityGroups` method. Security
groups added in this way will not be managed by the `Connections` object of the cluster.

```python
# vpc: ec2.Vpc
# cluster: docdb.DatabaseCluster


security_group = ec2.SecurityGroup(self, "SecurityGroup",
    vpc=vpc
)
cluster.add_security_groups(security_group)
```

## Deletion protection

Deletion protection can be enabled on an Amazon DocumentDB cluster to prevent accidental deletion of the cluster:

```python
# vpc: ec2.Vpc

cluster = docdb.DatabaseCluster(self, "Database",
    master_user=docdb.Login(
        username="myuser"
    ),
    instance_type=ec2.InstanceType.of(ec2.InstanceClass.R5, ec2.InstanceSize.LARGE),
    vpc_subnets=ec2.SubnetSelection(
        subnet_type=ec2.SubnetType.PUBLIC
    ),
    vpc=vpc,
    deletion_protection=True
)
```

## Rotating credentials

When the master password is generated and stored in AWS Secrets Manager, it can be rotated automatically:

```python
# cluster: docdb.DatabaseCluster

cluster.add_rotation_single_user()
```

```python
cluster = docdb.DatabaseCluster(stack, "Database",
    master_user=docdb.Login(
        username="docdb"
    ),
    instance_type=ec2.InstanceType.of(ec2.InstanceClass.R5, ec2.InstanceSize.LARGE),
    vpc=vpc,
    removal_policy=cdk.RemovalPolicy.DESTROY
)

cluster.add_rotation_single_user()
```

The multi user rotation scheme is also available:

```python
import aws_cdk.aws_secretsmanager as secretsmanager

# my_imported_secret: secretsmanager.Secret
# cluster: docdb.DatabaseCluster


cluster.add_rotation_multi_user("MyUser",
    secret=my_imported_secret
)
```

It's also possible to create user credentials together with the cluster and add rotation:

```python
# cluster: docdb.DatabaseCluster

my_user_secret = docdb.DatabaseSecret(self, "MyUserSecret",
    username="myuser",
    master_secret=cluster.secret
)
my_user_secret_attached = my_user_secret.attach(cluster) # Adds DB connections information in the secret

cluster.add_rotation_multi_user("MyUser",  # Add rotation using the multi user scheme
    secret=my_user_secret_attached)
```

**Note**: This user must be created manually in the database using the master credentials.
The rotation will start as soon as this user exists.

See also [@aws-cdk/aws-secretsmanager](https://github.com/aws/aws-cdk/blob/master/packages/%40aws-cdk/aws-secretsmanager/README.md) for credentials rotation of existing clusters.

## Audit and profiler Logs

Sending audit or profiler needs to be configured in two places:

1. Check / create the needed options in your ParameterGroup for [audit](https://docs.aws.amazon.com/documentdb/latest/developerguide/event-auditing.html#event-auditing-enabling-auditing) and
   [profiler](https://docs.aws.amazon.com/documentdb/latest/developerguide/profiling.html#profiling.enable-profiling) logs.
2. Enable the corresponding option(s) when creating the `DatabaseCluster`:

```python
import aws_cdk.aws_iam as iam
import aws_cdk.aws_logs as logs

# my_logs_publishing_role: iam.Role
# vpc: ec2.Vpc


cluster = docdb.DatabaseCluster(self, "Database",
    master_user=docdb.Login(
        username="myuser"
    ),
    instance_type=ec2.InstanceType.of(ec2.InstanceClass.R5, ec2.InstanceSize.LARGE),
    vpc_subnets=ec2.SubnetSelection(
        subnet_type=ec2.SubnetType.PUBLIC
    ),
    vpc=vpc,
    export_profiler_logs_to_cloud_watch=True,  # Enable sending profiler logs
    export_audit_logs_to_cloud_watch=True,  # Enable sending audit logs
    cloud_watch_logs_retention=logs.RetentionDays.THREE_MONTHS,  # Optional - default is to never expire logs
    cloud_watch_logs_retention_role=my_logs_publishing_role
)
```
