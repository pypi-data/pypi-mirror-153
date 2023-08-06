# CDK Construct library for higher-level ECS Constructs

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This library provides higher-level Amazon ECS constructs which follow common architectural patterns. It contains:

* Application Load Balanced Services
* Network Load Balanced Services
* Queue Processing Services
* Scheduled Tasks (cron jobs)
* Additional Examples

## Application Load Balanced Services

To define an Amazon ECS service that is behind an application load balancer, instantiate one of the following:

* `ApplicationLoadBalancedEc2Service`

```python
# cluster: ecs.Cluster

load_balanced_ecs_service = ecs_patterns.ApplicationLoadBalancedEc2Service(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=1024,
    task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageOptions(
        image=ecs.ContainerImage.from_registry("test"),
        environment={
            "TEST_ENVIRONMENT_VARIABLE1": "test environment variable 1 value",
            "TEST_ENVIRONMENT_VARIABLE2": "test environment variable 2 value"
        }
    ),
    desired_count=2
)
```

* `ApplicationLoadBalancedFargateService`

```python
# cluster: ecs.Cluster

load_balanced_fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=1024,
    cpu=512,
    task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageOptions(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    )
)

load_balanced_fargate_service.target_group.configure_health_check(
    path="/custom-health-path"
)
```

Instead of providing a cluster you can specify a VPC and CDK will create a new ECS cluster.
If you deploy multiple services CDK will only create one cluster per VPC.

You can omit `cluster` and `vpc` to let CDK create a new VPC with two AZs and create a cluster inside this VPC.

You can customize the health check for your target group; otherwise it defaults to `HTTP` over port `80` hitting path `/`.

Fargate services will use the `LATEST` platform version by default, but you can override by providing a value for the `platformVersion` property in the constructor.

Fargate services use the default VPC Security Group unless one or more are provided using the `securityGroups` property in the constructor.

By setting `redirectHTTP` to true, CDK will automatically create a listener on port 80 that redirects HTTP traffic to the HTTPS port.

If you specify the option `recordType` you can decide if you want the construct to use CNAME or Route53-Aliases as record sets.

If you need to encrypt the traffic between the load balancer and the ECS tasks, you can set the `targetProtocol` to `HTTPS`.

Additionally, if more than one application target group are needed, instantiate one of the following:

* `ApplicationMultipleTargetGroupsEc2Service`

```python
# One application load balancer with one listener and two target groups.
# cluster: ecs.Cluster

load_balanced_ec2_service = ecs_patterns.ApplicationMultipleTargetGroupsEc2Service(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=256,
    task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageProps(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    ),
    target_groups=[ecsPatterns.ApplicationTargetProps(
        container_port=80
    ), ecsPatterns.ApplicationTargetProps(
        container_port=90,
        path_pattern="a/b/c",
        priority=10
    )
    ]
)
```

* `ApplicationMultipleTargetGroupsFargateService`

```python
# One application load balancer with one listener and two target groups.
# cluster: ecs.Cluster

load_balanced_fargate_service = ecs_patterns.ApplicationMultipleTargetGroupsFargateService(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=1024,
    cpu=512,
    task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageProps(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    ),
    target_groups=[ecsPatterns.ApplicationTargetProps(
        container_port=80
    ), ecsPatterns.ApplicationTargetProps(
        container_port=90,
        path_pattern="a/b/c",
        priority=10
    )
    ]
)
```

## Network Load Balanced Services

To define an Amazon ECS service that is behind a network load balancer, instantiate one of the following:

* `NetworkLoadBalancedEc2Service`

```python
# cluster: ecs.Cluster

load_balanced_ecs_service = ecs_patterns.NetworkLoadBalancedEc2Service(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=1024,
    task_image_options=ecsPatterns.NetworkLoadBalancedTaskImageOptions(
        image=ecs.ContainerImage.from_registry("test"),
        environment={
            "TEST_ENVIRONMENT_VARIABLE1": "test environment variable 1 value",
            "TEST_ENVIRONMENT_VARIABLE2": "test environment variable 2 value"
        }
    ),
    desired_count=2
)
```

* `NetworkLoadBalancedFargateService`

```python
# cluster: ecs.Cluster

load_balanced_fargate_service = ecs_patterns.NetworkLoadBalancedFargateService(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=1024,
    cpu=512,
    task_image_options=ecsPatterns.NetworkLoadBalancedTaskImageOptions(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    )
)
```

The CDK will create a new Amazon ECS cluster if you specify a VPC and omit `cluster`. If you deploy multiple services the CDK will only create one cluster per VPC.

If `cluster` and `vpc` are omitted, the CDK creates a new VPC with subnets in two Availability Zones and a cluster within this VPC.

If you specify the option `recordType` you can decide if you want the construct to use CNAME or Route53-Aliases as record sets.

Additionally, if more than one network target group is needed, instantiate one of the following:

* NetworkMultipleTargetGroupsEc2Service

```python
# Two network load balancers, each with their own listener and target group.
# cluster: ecs.Cluster

load_balanced_ec2_service = ecs_patterns.NetworkMultipleTargetGroupsEc2Service(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=256,
    task_image_options=ecsPatterns.NetworkLoadBalancedTaskImageProps(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    ),
    load_balancers=[ecsPatterns.NetworkLoadBalancerProps(
        name="lb1",
        listeners=[ecsPatterns.NetworkListenerProps(
            name="listener1"
        )
        ]
    ), ecsPatterns.NetworkLoadBalancerProps(
        name="lb2",
        listeners=[ecsPatterns.NetworkListenerProps(
            name="listener2"
        )
        ]
    )
    ],
    target_groups=[ecsPatterns.NetworkTargetProps(
        container_port=80,
        listener="listener1"
    ), ecsPatterns.NetworkTargetProps(
        container_port=90,
        listener="listener2"
    )
    ]
)
```

* NetworkMultipleTargetGroupsFargateService

```python
# Two network load balancers, each with their own listener and target group.
# cluster: ecs.Cluster

load_balanced_fargate_service = ecs_patterns.NetworkMultipleTargetGroupsFargateService(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=512,
    task_image_options=ecsPatterns.NetworkLoadBalancedTaskImageProps(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    ),
    load_balancers=[ecsPatterns.NetworkLoadBalancerProps(
        name="lb1",
        listeners=[ecsPatterns.NetworkListenerProps(
            name="listener1"
        )
        ]
    ), ecsPatterns.NetworkLoadBalancerProps(
        name="lb2",
        listeners=[ecsPatterns.NetworkListenerProps(
            name="listener2"
        )
        ]
    )
    ],
    target_groups=[ecsPatterns.NetworkTargetProps(
        container_port=80,
        listener="listener1"
    ), ecsPatterns.NetworkTargetProps(
        container_port=90,
        listener="listener2"
    )
    ]
)
```

## Queue Processing Services

To define a service that creates a queue and reads from that queue, instantiate one of the following:

* `QueueProcessingEc2Service`

```python
# cluster: ecs.Cluster

queue_processing_ec2_service = ecs_patterns.QueueProcessingEc2Service(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=1024,
    image=ecs.ContainerImage.from_registry("test"),
    command=["-c", "4", "amazon.com"],
    enable_logging=False,
    desired_task_count=2,
    environment={
        "TEST_ENVIRONMENT_VARIABLE1": "test environment variable 1 value",
        "TEST_ENVIRONMENT_VARIABLE2": "test environment variable 2 value"
    },
    max_scaling_capacity=5,
    container_name="test"
)
```

* `QueueProcessingFargateService`

```python
# cluster: ecs.Cluster

queue_processing_fargate_service = ecs_patterns.QueueProcessingFargateService(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=512,
    image=ecs.ContainerImage.from_registry("test"),
    command=["-c", "4", "amazon.com"],
    enable_logging=False,
    desired_task_count=2,
    environment={
        "TEST_ENVIRONMENT_VARIABLE1": "test environment variable 1 value",
        "TEST_ENVIRONMENT_VARIABLE2": "test environment variable 2 value"
    },
    max_scaling_capacity=5,
    container_name="test"
)
```

when queue not provided by user, CDK will create a primary queue and a dead letter queue with default redrive policy and attach permission to the task to be able to access the primary queue.

## Scheduled Tasks

To define a task that runs periodically, there are 2 options:

* `ScheduledEc2Task`

```python
# Instantiate an Amazon EC2 Task to run at a scheduled interval
# cluster: ecs.Cluster

ecs_scheduled_task = ecs_patterns.ScheduledEc2Task(self, "ScheduledTask",
    cluster=cluster,
    scheduled_ec2_task_image_options=ecsPatterns.ScheduledEc2TaskImageOptions(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
        memory_limit_mi_b=256,
        environment={"name": "TRIGGER", "value": "CloudWatch Events"}
    ),
    schedule=appscaling.Schedule.expression("rate(1 minute)"),
    enabled=True,
    rule_name="sample-scheduled-task-rule"
)
```

* `ScheduledFargateTask`

```python
# cluster: ecs.Cluster

scheduled_fargate_task = ecs_patterns.ScheduledFargateTask(self, "ScheduledFargateTask",
    cluster=cluster,
    scheduled_fargate_task_image_options=ecsPatterns.ScheduledFargateTaskImageOptions(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
        memory_limit_mi_b=512
    ),
    schedule=appscaling.Schedule.expression("rate(1 minute)"),
    platform_version=ecs.FargatePlatformVersion.LATEST
)
```

## Additional Examples

In addition to using the constructs, users can also add logic to customize these constructs:

### Configure HTTPS on an ApplicationLoadBalancedFargateService

```python
from aws_cdk.aws_route53 import HostedZone
from aws_cdk.aws_certificatemanager import Certificate
from aws_cdk.aws_elasticloadbalancingv2 import SslPolicy

# vpc: ec2.Vpc
# cluster: ecs.Cluster


domain_zone = HostedZone.from_lookup(self, "Zone", domain_name="example.com")
certificate = Certificate.from_certificate_arn(self, "Cert", "arn:aws:acm:us-east-1:123456:certificate/abcdefg")
load_balanced_fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "Service",
    vpc=vpc,
    cluster=cluster,
    certificate=certificate,
    ssl_policy=SslPolicy.RECOMMENDED,
    domain_name="api.example.com",
    domain_zone=domain_zone,
    redirect_hTTP=True,
    task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageOptions(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    )
)
```

### Add Schedule-Based Auto-Scaling to an ApplicationLoadBalancedFargateService

```python
# cluster: ecs.Cluster

load_balanced_fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=1024,
    desired_count=1,
    cpu=512,
    task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageOptions(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    )
)

scalable_target = load_balanced_fargate_service.service.auto_scale_task_count(
    min_capacity=5,
    max_capacity=20
)

scalable_target.scale_on_schedule("DaytimeScaleDown",
    schedule=appscaling.Schedule.cron(hour="8", minute="0"),
    min_capacity=1
)

scalable_target.scale_on_schedule("EveningRushScaleUp",
    schedule=appscaling.Schedule.cron(hour="20", minute="0"),
    min_capacity=10
)
```

### Add Metric-Based Auto-Scaling to an ApplicationLoadBalancedFargateService

```python
# cluster: ecs.Cluster

load_balanced_fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=1024,
    desired_count=1,
    cpu=512,
    task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageOptions(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    )
)

scalable_target = load_balanced_fargate_service.service.auto_scale_task_count(
    min_capacity=1,
    max_capacity=20
)

scalable_target.scale_on_cpu_utilization("CpuScaling",
    target_utilization_percent=50
)

scalable_target.scale_on_memory_utilization("MemoryScaling",
    target_utilization_percent=50
)
```

### Change the default Deployment Controller

```python
# cluster: ecs.Cluster

load_balanced_fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=1024,
    desired_count=1,
    cpu=512,
    task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageOptions(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    ),
    deployment_controller=ecs.DeploymentController(
        type=ecs.DeploymentControllerType.CODE_DEPLOY
    )
)
```

### Deployment circuit breaker and rollback

Amazon ECS [deployment circuit breaker](https://aws.amazon.com/tw/blogs/containers/announcing-amazon-ecs-deployment-circuit-breaker/)
automatically rolls back unhealthy service deployments without the need for manual intervention. Use `circuitBreaker` to enable
deployment circuit breaker and optionally enable `rollback` for automatic rollback. See [Using the deployment circuit breaker](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-ecs.html)
for more details.

```python
# cluster: ecs.Cluster

service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=1024,
    desired_count=1,
    cpu=512,
    task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageOptions(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    ),
    circuit_breaker=ecs.DeploymentCircuitBreaker(rollback=True)
)
```

### Set deployment configuration on QueueProcessingService

```python
# cluster: ecs.Cluster

queue_processing_fargate_service = ecs_patterns.QueueProcessingFargateService(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=512,
    image=ecs.ContainerImage.from_registry("test"),
    command=["-c", "4", "amazon.com"],
    enable_logging=False,
    desired_task_count=2,
    environment={},
    max_scaling_capacity=5,
    max_healthy_percent=200,
    min_healthy_percent=66
)
```

### Set taskSubnets and securityGroups for QueueProcessingFargateService

```python
# vpc: ec2.Vpc
# security_group: ec2.SecurityGroup

queue_processing_fargate_service = ecs_patterns.QueueProcessingFargateService(self, "Service",
    vpc=vpc,
    memory_limit_mi_b=512,
    image=ecs.ContainerImage.from_registry("test"),
    security_groups=[security_group],
    task_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)
)
```

### Define tasks with public IPs for QueueProcessingFargateService

```python
# vpc: ec2.Vpc

queue_processing_fargate_service = ecs_patterns.QueueProcessingFargateService(self, "Service",
    vpc=vpc,
    memory_limit_mi_b=512,
    image=ecs.ContainerImage.from_registry("test"),
    assign_public_ip=True
)
```

### Define tasks with custom queue parameters for QueueProcessingFargateService

```python
# vpc: ec2.Vpc

queue_processing_fargate_service = ecs_patterns.QueueProcessingFargateService(self, "Service",
    vpc=vpc,
    memory_limit_mi_b=512,
    image=ecs.ContainerImage.from_registry("test"),
    max_receive_count=42,
    retention_period=Duration.days(7),
    visibility_timeout=Duration.minutes(5)
)
```

### Set capacityProviderStrategies for QueueProcessingFargateService

```python
# cluster: ecs.Cluster

cluster.enable_fargate_capacity_providers()

queue_processing_fargate_service = ecs_patterns.QueueProcessingFargateService(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=512,
    image=ecs.ContainerImage.from_registry("test"),
    capacity_provider_strategies=[ecs.CapacityProviderStrategy(
        capacity_provider="FARGATE_SPOT",
        weight=2
    ), ecs.CapacityProviderStrategy(
        capacity_provider="FARGATE",
        weight=1
    )
    ]
)
```

### Set a custom container-level Healthcheck for QueueProcessingFargateService

```python
# vpc: ec2.Vpc
# security_group: ec2.SecurityGroup

queue_processing_fargate_service = ecs_patterns.QueueProcessingFargateService(self, "Service",
    vpc=vpc,
    memory_limit_mi_b=512,
    image=ecs.ContainerImage.from_registry("test"),
    health_check=ecs.HealthCheck(
        command=["CMD-SHELL", "curl -f http://localhost/ || exit 1"],
        # the properties below are optional
        interval=Duration.minutes(30),
        retries=123,
        start_period=Duration.minutes(30),
        timeout=Duration.minutes(30)
    )
)
```

### Set capacityProviderStrategies for QueueProcessingEc2Service

```python
import aws_cdk.aws_autoscaling as autoscaling


vpc = ec2.Vpc(self, "Vpc", max_azs=1)
cluster = ecs.Cluster(self, "EcsCluster", vpc=vpc)
auto_scaling_group = autoscaling.AutoScalingGroup(self, "asg",
    vpc=vpc,
    instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
    machine_image=ecs.EcsOptimizedImage.amazon_linux2()
)
capacity_provider = ecs.AsgCapacityProvider(self, "provider",
    auto_scaling_group=auto_scaling_group
)
cluster.add_asg_capacity_provider(capacity_provider)

queue_processing_fargate_service = ecs_patterns.QueueProcessingFargateService(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=512,
    image=ecs.ContainerImage.from_registry("test"),
    capacity_provider_strategies=[ecs.CapacityProviderStrategy(
        capacity_provider=capacity_provider.capacity_provider_name
    )
    ]
)
```

### Select specific vpc subnets for ApplicationLoadBalancedFargateService

```python
# cluster: ecs.Cluster

load_balanced_fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=1024,
    desired_count=1,
    cpu=512,
    task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageOptions(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    ),
    task_subnets=ec2.SubnetSelection(
        subnets=[ec2.Subnet.from_subnet_id(self, "subnet", "VpcISOLATEDSubnet1Subnet80F07FA0")]
    )
)
```

### Set PlatformVersion for ScheduledFargateTask

```python
# cluster: ecs.Cluster

scheduled_fargate_task = ecs_patterns.ScheduledFargateTask(self, "ScheduledFargateTask",
    cluster=cluster,
    scheduled_fargate_task_image_options=ecsPatterns.ScheduledFargateTaskImageOptions(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
        memory_limit_mi_b=512
    ),
    schedule=appscaling.Schedule.expression("rate(1 minute)"),
    platform_version=ecs.FargatePlatformVersion.VERSION1_4
)
```

### Set SecurityGroups for ScheduledFargateTask

```python
vpc = ec2.Vpc(self, "Vpc", max_azs=1)
cluster = ecs.Cluster(self, "EcsCluster", vpc=vpc)
security_group = ec2.SecurityGroup(self, "SG", vpc=vpc)

scheduled_fargate_task = ecs_patterns.ScheduledFargateTask(self, "ScheduledFargateTask",
    cluster=cluster,
    scheduled_fargate_task_image_options=ecsPatterns.ScheduledFargateTaskImageOptions(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
        memory_limit_mi_b=512
    ),
    schedule=appscaling.Schedule.expression("rate(1 minute)"),
    security_groups=[security_group]
)
```

### Use the REMOVE_DEFAULT_DESIRED_COUNT feature flag

The REMOVE_DEFAULT_DESIRED_COUNT feature flag is used to override the default desiredCount that is autogenerated by the CDK. This will set the desiredCount of any service created by any of the following constructs to be undefined.

* ApplicationLoadBalancedEc2Service
* ApplicationLoadBalancedFargateService
* NetworkLoadBalancedEc2Service
* NetworkLoadBalancedFargateService
* QueueProcessingEc2Service
* QueueProcessingFargateService

If a desiredCount is not passed in as input to the above constructs, CloudFormation will either create a new service to start up with a desiredCount of 1, or update an existing service to start up with the same desiredCount as prior to the update.

To enable the feature flag, ensure that the REMOVE_DEFAULT_DESIRED_COUNT flag within an application stack context is set to true, like so:

```python
# stack: Stack

stack.node.set_context(cxapi.ECS_REMOVE_DEFAULT_DESIRED_COUNT, True)
```

The following is an example of an application with the REMOVE_DEFAULT_DESIRED_COUNT feature flag enabled:

```python
from aws_cdk.core import App, Stack
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_ecs as ecs
import aws_cdk.aws_ecs_patterns as ecs_patterns
import aws_cdk.cx_api as cxapi
import path as path

app = App()

stack = Stack(app, "aws-ecs-patterns-queue")
stack.node.set_context(cxapi.ECS_REMOVE_DEFAULT_DESIRED_COUNT, True)

vpc = ec2.Vpc(stack, "VPC",
    max_azs=2
)

ecs_patterns.QueueProcessingFargateService(stack, "QueueProcessingService",
    vpc=vpc,
    memory_limit_mi_b=512,
    image=ecs.AssetImage(path.join(__dirname, "..", "sqs-reader"))
)
```

### Deploy application and metrics sidecar

The following is an example of deploying an application along with a metrics sidecar container that utilizes `dockerLabels` for discovery:

```python
# cluster: ecs.Cluster
# vpc: ec2.Vpc

service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "Service",
    cluster=cluster,
    vpc=vpc,
    desired_count=1,
    task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageOptions(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
        docker_labels={
            "application.label.one": "first_label",
            "application.label.two": "second_label"
        }
    )
)

service.task_definition.add_container("Sidecar",
    image=ecs.ContainerImage.from_registry("example/metrics-sidecar")
)
```

### Select specific load balancer name ApplicationLoadBalancedFargateService

```python
# cluster: ecs.Cluster

load_balanced_fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=1024,
    desired_count=1,
    cpu=512,
    task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageOptions(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    ),
    task_subnets=ec2.SubnetSelection(
        subnets=[ec2.Subnet.from_subnet_id(self, "subnet", "VpcISOLATEDSubnet1Subnet80F07FA0")]
    ),
    load_balancer_name="application-lb-name"
)
```
