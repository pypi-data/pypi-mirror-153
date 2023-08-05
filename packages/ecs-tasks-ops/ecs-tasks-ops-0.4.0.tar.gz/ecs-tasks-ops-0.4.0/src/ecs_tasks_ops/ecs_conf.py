"""Configuration file for ecs-task-ops."""
import json
import os

cfg = {}


def load_config():
    """Load configuration json file for this application."""
    global cfg, cfg_path
    for loc in (
        os.curdir,
        os.path.expanduser("~"),
        os.path.expanduser("~/.config/ecs-tasks-ops"),
        "/etc/ecs-tasks-ops",
        os.environ.get("ECS_TASKS_OPS_CONF"),
    ):
        try:
            if not loc:
                continue
            cfg_path = os.path.join(loc, "ecs-tasks-ops.json")
            with open(cfg_path) as source:
                print(f"Loading data from {cfg_path}")
                cfg = json.load(source)
        except IOError:
            pass
