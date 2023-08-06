"""Generate ssh commands to access to ECS resources."""


def ssh_cmd_container_instance(detail) -> str:
    """SSH command to access a ecs2 instance by id."""
    return f"TERM=xterm ssh {detail['ec2InstanceId']}"


def ssh_cmd_task_log(detail) -> str:
    """SSH command to access the first docker instance logs of a task."""
    return f"TERM=xterm ssh {detail['ec2InstanceId']} docker logs -f --tail=100 {detail['containers'][0]['runtimeId']}"


def ssh_cmd_task_exec(detail, command_on_docker, wait_press_key=None) -> str:
    """SSH command to execute a command inside the first docker containter of a task."""
    wait_cmd = ""
    if wait_press_key:
        wait_cmd = "; echo 'Press a key'; read q"
    return (
        f"TERM=xterm ssh -t {detail['ec2InstanceId']} docker exec -ti {detail['containers'][0]['runtimeId']} {command_on_docker}"
        + wait_cmd
    )


def ssh_cmd_docker_container_log(detail) -> str:
    """SSH command to access a docker instance logs."""
    return f"TERM=xterm ssh {detail['ec2InstanceId']} docker logs -f --tail=100 {detail['runtimeId']}"


def ssh_cmd_docker_container_exec(
    detail, command_on_docker, wait_press_key=None
) -> str:
    """SSH command to execute a command inside a docker containter."""
    wait_cmd = ""
    if wait_press_key:
        wait_cmd = "; echo 'Press a key'; read q"
    return (
        f"TERM=xterm ssh -t {detail['ec2InstanceId']} docker exec -ti {detail['runtimeId']} {command_on_docker}"
        + wait_cmd
    )
