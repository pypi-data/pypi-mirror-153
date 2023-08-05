"""Command-line interface."""
import click

from ecs_tasks_ops import ecs_data
from ecs_tasks_ops import ecs_facade
from ecs_tasks_ops import pretty_json
from ecs_tasks_ops import pretty_table


@click.group()
@click.option("-x", "--debug/--no-debug", default=False)
@click.option("-j", "--output-json", "output_json", is_flag=True, default=False)
@click.version_option()
@click.pass_context
def main(ctx, debug, output_json) -> None:
    """Ecs Tasks Ops."""
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug
    # TODO: Format output with json
    ctx.obj["OUT_JSON"] = output_json


@main.command("clusters")
@click.pass_context
def main_clusters(ctx):
    """Clusters information."""
    clusters = ecs_data.get_clusters()
    if ctx.obj["OUT_JSON"]:
        click.echo(pretty_json.dumps(clusters))
    else:
        click.echo(pretty_table.tabulate_list_json(clusters, fields_to=7))


@main.command("services")
@click.option("-c", "--cluster-name", default="default", help="Cluster name")
@click.pass_context
def main_services(ctx, cluster_name):
    """Services defined in a cluster."""
    try:
        services_info = ecs_data.get_services(cluster_name)
        if ctx.obj["OUT_JSON"]:
            click.echo(pretty_json.dumps(services_info))
        else:
            click.echo(
                pretty_table.tabulate_list_json_keys(
                    services_info,
                    [
                        "serviceArn",
                        "serviceName",
                        "status",
                        "runningCount",
                        "desiredCount",
                    ],
                )
            )

    except ecs_facade.ecs_client().exceptions.ClusterNotFoundException:
        click.secho(f"Cluster {cluster_name} not found", fg="red")
        return []
    except Exception:
        click.secho("There has been an error.", fg="red")
        return []


@main.command("container-instances")
@click.option("-c", "--cluster-name", default="default", help="Cluster name")
@click.pass_context
def main_container_instances(ctx, cluster_name):
    """Container instances defined in a cluster."""
    try:
        container_instances_info = ecs_data.get_containers_instances(cluster_name)
        if ctx.obj["OUT_JSON"]:
            click.echo(pretty_json.dumps(container_instances_info))
        else:
            click.echo(
                pretty_table.tabulate_list_json_keys(
                    container_instances_info, ["ec2InstanceId", "versionInfo"]
                )
            )

    except ecs_facade.ecs_client().exceptions.ClusterNotFoundException:
        click.secho(f"Cluster {cluster_name} not found", fg="red")
        return []
    except Exception:
        click.secho("There has been an error.", fg="red")
        return []


@main.command("tasks")
@click.option("-c", "--cluster-name", default="default", help="Cluster name")
@click.option("-s", "--service-name", help="Service name")
@click.option("-i", "--container-instance", help="Container instance")
@click.pass_context
def main_tasks(ctx, cluster_name, service_name, container_instance):
    """Set tasks defined in a cluster."""
    try:
        if not service_name and not container_instance:
            tasks_info = ecs_data.get_tasks_cluster(cluster_name)
        elif service_name:
            tasks_info = ecs_data.get_tasks_service(cluster_name, service_name)
        elif container_instance:
            tasks_info = ecs_data.get_tasks_container_instance(
                cluster_name, container_instance
            )

        if ctx.obj["OUT_JSON"]:
            click.echo(pretty_json.dumps(tasks_info))
        else:
            click.echo(
                pretty_table.tabulate_list_json_keys(
                    tasks_info,
                    [
                        "name",
                        "taskArn",
                        "ec2InstanceId",
                        "availabilityZone",
                        "memory",
                        "cpu",
                        "desiredStatus",
                        "healthStatus",
                        "lastStatus",
                    ],
                )
            )

    except ecs_facade.ecs_client().exceptions.ClusterNotFoundException:
        click.secho(f"Cluster {cluster_name} not found", fg="red")
        return []
    except Exception:
        click.secho("There has been an error.", fg="red")
        return []


@main.command("containers")
@click.option("-c", "--cluster-name", default="default", help="Cluster name")
@click.option("-s", "--service-name", help="Service name", required=True)
@click.option("-d", "--docker-name", help="Docker container name")
@click.pass_context
def main_containers(ctx, cluster_name, service_name, docker_name):
    """Get docker containers defined in a cluster."""
    try:
        containers_info = ecs_data.get_containers_service(cluster_name, service_name)

        if docker_name:
            containers_info = [c for c in containers_info if c["name"] == docker_name]

        if ctx.obj["OUT_JSON"]:
            click.echo(pretty_json.dumps(containers_info))
        else:
            click.echo(
                pretty_table.tabulate_list_json_keys(
                    containers_info,
                    [
                        "image",
                        "ec2InstanceId",
                        "name",
                        "memory",
                        "cpu",
                        "runtimeId",
                        "healthStatus",
                        "lastStatus",
                    ],
                )
            )

    except ecs_facade.ecs_client().exceptions.ClusterNotFoundException:
        click.secho(f"Cluster {cluster_name} not found", fg="red")
        return []
    except ecs_facade.ecs_client().exceptions.ServiceNotFoundException:
        click.secho(f"Service {service_name} not found", fg="red")
        return []
    except Exception:
        click.secho("There has been an error.", fg="red")
        return []


if __name__ == "__main__":
    # main(prog_name="ecs-tasks-ops")  # pragma: no cover
    pass
