"""ECS Facade for ecs-tasks-ops."""
from itertools import chain

import boto3

# ecs_client = boto3.client("ecs")


def ecs_client():
    """Get ecs client."""
    return boto3.client("ecs")


def get_ecs_list(operation_name, response_attribute, **operation_params):
    """Get a complete list of elements by operation_name."""
    paginator = ecs_client().get_paginator(operation_name)
    operation_params["PaginationConfig"] = {"MaxItems": 100}
    paginator_ite = paginator.paginate(**operation_params)
    return list(
        chain.from_iterable(
            [resp.get(response_attribute, []) for resp in paginator_ite]
        )
    )


def get_cluster_list():
    """Get a complete list with cluster information."""
    list_clusters = get_ecs_list("list_clusters", "clusterArns")
    return ecs_client().describe_clusters(clusters=list_clusters).get("clusters", [])


def get_describe_services(cluster_name, services_arns):
    """Get information about a list of services arns."""
    return (
        ecs_client()
        .describe_services(cluster=cluster_name, services=services_arns)
        .get("services", [])
    )


def get_describe_tasks(cluster_name, tasks_arns):
    """Get information about a list of tasks."""
    return (
        ecs_client()
        .describe_tasks(cluster=cluster_name, tasks=tasks_arns)
        .get("tasks", [])
    )


def get_describe_container_instances(cluster_name, container_instances_arns):
    """Get information about a list of container instances."""
    return (
        ecs_client()
        .describe_container_instances(
            cluster=cluster_name, containerInstances=container_instances_arns
        )
        .get("containerInstances", [])
    )


def get_all_services(cluster_name):
    """Get information about all services defined in a cluster."""
    list_services_arns = get_ecs_list(
        "list_services", "serviceArns", cluster=cluster_name
    )
    # Max request per describe_services are 10 services arns, so we slice them 10 by 10, and request each 10
    slices = [slice(i, i + 10, 1) for i in range(0, len(list_services_arns), 10)]
    services = list(
        chain.from_iterable(
            [
                get_describe_services(cluster_name, list_services_arns[slc])
                for slc in slices
            ]
        )
    )
    return services


def get_all_container_instances(cluster_name):
    """Get information about all container instances defined in a cluster."""
    list_container_instances_arns = get_ecs_list(
        "list_container_instances", "containerInstanceArns", cluster=cluster_name
    )
    # Max request per describe_services are 10 services arns, so we slice them 100 by 100, and request each 100
    slices = [
        slice(i, i + 100, 1) for i in range(0, len(list_container_instances_arns), 100)
    ]
    containers_instances = list(
        chain.from_iterable(
            [
                get_describe_container_instances(
                    cluster_name, list_container_instances_arns[slc]
                )
                for slc in slices
            ]
        )
    )
    return containers_instances


def get_all_tasks_cluster(cluster_name):
    """Get information about all tasks defined in a cluster for a service."""
    list_tasks_arns = get_ecs_list("list_tasks", "taskArns", cluster=cluster_name)
    # Max request per describe_services are 100 services arns, so we slice them 100 by 100, and request each 100
    slices = [slice(i, i + 100, 1) for i in range(0, len(list_tasks_arns), 100)]
    tasks = list(
        chain.from_iterable(
            [get_describe_tasks(cluster_name, list_tasks_arns[slc]) for slc in slices]
        )
    )
    return tasks


def get_all_tasks_services(cluster_name, service_name):
    """Get information about all tasks defined in a cluster for a service."""
    list_tasks_arns = get_ecs_list(
        "list_tasks", "taskArns", cluster=cluster_name, serviceName=service_name
    )
    # Max request per describe_services are 100 services arns, so we slice them 100 by 100, and request each 100
    slices = [slice(i, i + 100, 1) for i in range(0, len(list_tasks_arns), 100)]
    tasks = list(
        chain.from_iterable(
            [get_describe_tasks(cluster_name, list_tasks_arns[slc]) for slc in slices]
        )
    )
    return tasks


def get_all_tasks_container(cluster_name, container_arn):
    """Get information about all tasks defined in a cluster for a service."""
    list_tasks_arns = get_ecs_list(
        "list_tasks", "taskArns", cluster=cluster_name, containerInstance=container_arn
    )
    # Max request per describe_services are 100 services arns, so we slice them 100 by 100, and request each 100
    slices = [slice(i, i + 100, 1) for i in range(0, len(list_tasks_arns), 100)]
    tasks = list(
        chain.from_iterable(
            [get_describe_tasks(cluster_name, list_tasks_arns[slc]) for slc in slices]
        )
    )
    return tasks


def stop_task(cluster_name, task_arn, reason=""):
    """Stop a specific task."""
    return (
        ecs_client()
        .stop_task(cluster=cluster_name, task=task_arn, reason=reason)
        .get("task", {})
    )


def restart_service(cluster_name, service_arn, force_new_deployment=False):
    """Stop a specific task."""
    return (
        ecs_client()
        .update_service(
            cluster=cluster_name,
            service=service_arn,
            forceNewDeployment=force_new_deployment,
        )
        .get("service", {})
    )
