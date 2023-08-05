"""Qt5 Tree Model for ecs."""
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from ecs_tasks_ops import ecs_conf
from ecs_tasks_ops import ecs_data
from ecs_tasks_ops import ecs_facade
from ecs_tasks_ops import ecs_ssh
from ecs_tasks_ops import pretty_json


class ECSTreeItem(QtWidgets.QTreeWidgetItem):
    """Tree Widgets Item for ECS elements."""

    def __init__(self, name, identifier, detail_type, detail, parent=None):
        """Initialization of basic ECS element, with name, arn_id, type and json data."""
        super(ECSTreeItem, self).__init__(parent, [name, identifier])
        self.name = name
        self.identifier = identifier
        self.detail_type = detail_type
        self.detail = detail

    def refresh_children(self):
        """Refresh list of children elements."""
        pass

    def get_attributes(self):
        """Get a list of basic attributes for detail view."""
        return [
            ("Name", self.name),
            ("Identifier", self.identifier),
            ("Detail Type", self.detail_type),
        ]

    def clear_children(self):
        """Clear list of children elements."""
        for i in reversed(range(self.childCount())):
            self.removeChild(self.child(i))

    def get_context_menu(self, menu):
        """Get basic context menu with mouse right-button."""
        menu.addSeparator()
        menu.addAction("Refresh Children", self.refresh_children)
        menu.addAction("Show Detail", self.command_show_detail)

    def command_show_detail(self):
        """Update detail view with this elements."""
        self.treeWidget().command_show_detail(self)


class ECSClusterTreeItem(ECSTreeItem):
    """Tree Widgets Item for Clusters elements."""

    def __init__(self, detail, parent=None):
        """Initialize Cluster item."""
        super(ECSClusterTreeItem, self).__init__(
            name=detail["clusterName"],
            identifier=detail["clusterArn"],
            detail_type="cluster",
            detail=detail,
            parent=parent,
        )

    def refresh_children(self):
        """Refresh cluster children with available options."""
        self.clear_children()
        self.addChild(ECSListTasksClusterTreeItem(self.detail, self))
        self.addChild(ECSListServicesClusterTreeItem(self.detail, self))
        self.addChild(ECSListContainersClusterTreeItem(self.detail, self))

    def get_attributes(self):
        """Get a list of basic attributes for cluters."""
        return [
            ("Name", self.name),
            ("Identifier", self.identifier),
            ("Detail Type", self.detail_type),
            ("Status", self.detail["status"]),
            ("Active Services", self.detail["activeServicesCount"]),
            ("Running Tasks", self.detail["runningTasksCount"]),
            ("Pending Tasks", self.detail["pendingTasksCount"]),
            ("Containers", self.detail["registeredContainerInstancesCount"]),
        ]


class ECSListServicesClusterTreeItem(ECSTreeItem):
    """Tree Widgets Item for List of Services of a cluster."""

    def __init__(self, detail, parent=None):
        """Initilize info to get a list of services for a cluster."""
        super(ECSListServicesClusterTreeItem, self).__init__(
            name=f"Services on '{detail['clusterName']}'",
            identifier=detail["clusterName"],
            detail_type="list_services",
            detail=detail,
            parent=parent,
        )

    def refresh_children(self):
        """Get a list of services for a cluster."""
        self.clear_children()
        for service in ecs_data.get_services(self.identifier):
            self.addChild(ECSServiceTreeItem(service, self))


class ECSListTasksClusterTreeItem(ECSTreeItem):
    """Tree Widgets Item for List of Tasks of a cluster."""

    def __init__(self, detail, parent=None):
        """Initialize info to get a list of tasks for a cluster."""
        super(ECSListTasksClusterTreeItem, self).__init__(
            name=f"Tasks on '{detail['clusterName']}'",
            identifier=detail["clusterName"],
            detail_type="list_services",
            detail=detail,
            parent=parent,
        )

    def refresh_children(self):
        """Get a list of tasks for a cluster."""
        self.clear_children()
        for task in ecs_data.get_tasks_cluster(self.identifier):
            self.addChild(ECSTaskTreeItem(task, self))


class ECSListContainersClusterTreeItem(ECSTreeItem):
    """Tree Widgets Item for List of Containers Instances of a cluster."""

    def __init__(self, detail, parent=None):
        """Initialize info to get a list of container instances for a cluster."""
        super(ECSListContainersClusterTreeItem, self).__init__(
            name=f"Containers on '{detail['clusterName']}'",
            identifier=detail["clusterName"],
            detail_type="list_services",
            detail=detail,
            parent=parent,
        )

    def refresh_children(self):
        """Get a list of container instances for a cluster."""
        self.clear_children()
        for container in ecs_data.get_containers_instances(self.identifier):
            self.addChild(ECSContainerTreeItem(container, self.identifier, self))


class ECSServiceTreeItem(ECSTreeItem):
    """Tree Widgets Item for Services elements."""

    def __init__(self, detail, parent=None):
        """Contains information about a service."""
        super(ECSServiceTreeItem, self).__init__(
            name=detail["serviceName"],
            identifier=detail["serviceArn"],
            detail_type="service",
            detail=detail,
            parent=parent,
        )
        self.cluster_identifier = detail["clusterArn"]

    def refresh_children(self):
        """Get a list of tasks for this service."""
        self.clear_children()
        for task in ecs_data.get_tasks_service(
            self.cluster_identifier, self.identifier
        ):
            self.addChild(ECSTaskTreeItem(task, self))

    def get_attributes(self):
        """Detail attributes view for this service."""
        deployment_config = self.detail["deploymentConfiguration"]
        min_bracket = deployment_config["minimumHealthyPercent"]
        max_bracket = deployment_config["maximumPercent"]

        return [
            ("Name", self.name),
            ("Identifier", self.identifier),
            ("Detail Type", self.detail_type),
            ("Status", self.detail["status"]),
            ("Task Definition", self.detail["taskDefinition"]),
            ("Running", self.detail["runningCount"]),
            ("Pending", self.detail["pendingCount"]),
            ("Desired", self.detail["desiredCount"]),
            (
                "Redeployment bracket",
                "Min: " + str(min_bracket) + "%, Max: " + str(max_bracket) + "%",
            ),
        ]

    def get_context_menu(self, menu):
        """Context menu for a service item."""
        menu.addAction("Show Events", self.command_service_show_events)
        menu.addAction("Force Restart Service", self.command_service_restart)
        super(ECSServiceTreeItem, self).get_context_menu(menu)

    def command_service_restart(self):
        """Send a restart command for this service."""
        self.treeWidget().command_service_restart(self)

    def command_service_show_events(self):
        """Open a list of events produced in this services."""
        self.treeWidget().command_service_show_events(self)


class ECSTaskTreeItem(ECSTreeItem):
    """Tree Widgets Item for Tasks elements."""

    def __init__(self, detail, parent=None):
        """Contains information about a task."""
        super(ECSTaskTreeItem, self).__init__(
            name=detail["name"],
            identifier=detail["taskArn"],
            detail_type="task",
            detail=detail,
            parent=parent,
        )
        self.cluster_identifier = self.detail["clusterArn"]

    def refresh_children(self):
        """Get a list of docker containers of this task."""
        self.clear_children()
        for task in ecs_data.get_containers_tasks(
            self.cluster_identifier, self.identifier
        ):
            self.addChild(
                ECSDockerContainerTreeItem(
                    task, self.identifier, self.cluster_identifier, self
                )
            )

    def get_attributes(self):
        """Get a list of attributes for detail view."""
        return [
            ("Name", self.name),
            ("Identifier", self.identifier),
            ("Detail Type", self.detail_type),
            ("Cluster Arn", self.detail["clusterArn"]),
            ("Status", self.detail["lastStatus"]),
            ("Desired Status", self.detail["desiredStatus"]),
            ("EC2 Instance", self.detail["ec2InstanceId"]),
            ("Availability Zone", self.detail["availabilityZone"]),
            ("Connectivity", self.detail.get("connectivity", "")),
            ("Task Definition", self.detail["taskDefinitionArn"]),
            (
                "Container Instance ID",
                self.detail["containerInstanceArn"].split("/", 1)[1],
            ),
            ("N. Docker images", len(self.detail["containers"])),
            ("Networks", "\n".join(self.detail["networks"])),
            ("Connectivity Time", self.detail["connectivityAt"]),
        ]

    def get_context_menu(self, menu):
        """Context menu for this task item."""
        menu.addAction("Stop Task", self.command_task_stop)
        menu.addAction("SSH Instance Container", self.command_container_ssh)
        menu.addAction("Docker Log (First Task)", self.command_task_log)
        super(ECSTaskTreeItem, self).get_context_menu(menu)

    def command_task_stop(self):
        """Send stop command to ECS for this task."""
        self.treeWidget().command_task_stop(self)

    def command_container_ssh(self):
        """Access to the continer instance of this tasks through ssh."""
        self.treeWidget().command_container_ssh(self)

    def command_task_log(self):
        """Show log info for the first docker container of this tasks."""
        self.treeWidget().command_task_log(self)


class ECSContainerTreeItem(ECSTreeItem):
    """Tree Widgets Item for Container Instances elements."""

    def __init__(self, detail, cluster_identifier, parent=None):
        """Contains information about container instances."""
        super(ECSContainerTreeItem, self).__init__(
            name=detail["ec2InstanceId"],
            identifier=detail["containerInstanceArn"],
            detail_type="container",
            detail=detail,
            parent=parent,
        )
        self.cluster_identifier = cluster_identifier

    def refresh_children(self):
        """Get a list of tasks of this container instance."""
        self.clear_children()
        for task in ecs_data.get_tasks_container_instance(
            self.cluster_identifier, self.identifier
        ):
            self.addChild(ECSTaskTreeItem(task, self))

    def get_attributes(self):
        """Get a list of attributes for detail view."""
        return [
            ("Name", self.name),
            ("Identifier", self.identifier),
            ("Detail Type", self.detail_type),
            ("Status", self.detail["status"]),
            ("EC2 Instance Id", self.detail["ec2InstanceId"]),
            ("Running Tasks", self.detail["runningTasksCount"]),
            ("Pending Tasks", self.detail["pendingTasksCount"]),
            ("AMI Id", self.detail["ami_id"]),
            ("Instance Type", self.detail["instance_type"]),
            ("Availability Zone", self.detail["availability_zone"]),
            (
                "Memory",
                "Available: "
                + str(self.detail["available_memory"])
                + " Total: "
                + str(self.detail["total_memory"]),
            ),
            (
                "CPU",
                "Available: "
                + str(self.detail["available_cpu"])
                + " Total: "
                + str(self.detail["total_cpu"]),
            ),
            ("Taken ports", self.detail["taken_ports"]),
        ]

    def get_context_menu(self, menu):
        """Context menu for container instances."""
        menu.addAction("SSH Instance Container", self.command_container_ssh)
        super(ECSContainerTreeItem, self).get_context_menu(menu)

    def command_container_ssh(self):
        """Access to this container instance through ssh."""
        self.treeWidget().command_container_ssh(self)


class ECSDockerContainerTreeItem(ECSTreeItem):
    """Tree Widgets Item for Docker Containers elements."""

    def __init__(self, detail, task_identifier, cluster_identifier, parent=None):
        """Contains information about docker container."""
        super(ECSDockerContainerTreeItem, self).__init__(
            name=detail["name"],
            identifier=detail["containerArn"],
            detail_type="docker_container",
            detail=detail,
            parent=parent,
        )
        self.cluster_identifier = cluster_identifier
        self.task_identifier = task_identifier

    # def refresh_children(self):
    #     self.clear_children()
    #     for task in ecs_data.get_tasks_container_instance(self.cluster_identifier, self.identifier):
    #         self.addChild(ECSTaskTreeItem(task, self))

    def get_attributes(self):
        """Get a list of attributes for detail view."""
        return [
            ("Name", self.name),
            ("Identifier", self.identifier),
            ("Detail Type", self.detail_type),
            ("Container Arn", self.detail["containerArn"]),
            ("Status", self.detail["lastStatus"]),
            ("Health Status", self.detail["healthStatus"]),
            ("Docker id", self.detail["runtimeId"]),
            ("Docker Image", self.detail["image"]),
            ("CPU", self.detail["cpu"]),
            # ('Memory Reservation', self.detail['memoryReservation']),
            ("Instance ID", self.detail["ec2InstanceId"]),
            ("Networks", self.detail["networks"]),
        ]

    def get_context_menu(self, menu):
        """Context menu for docker containers."""
        menu.addAction("SSH Instance Container", self.command_container_ssh)
        menu.addAction("Docker log", self.command_docker_log)
        menu.addAction("Docker exec", self.command_docker_exec)
        super(ECSDockerContainerTreeItem, self).get_context_menu(menu)

    def command_container_ssh(self):
        """Access to container instances server which contains this docker container."""
        self.treeWidget().command_container_ssh(self)

    def command_docker_log(self):
        """Show log information of this docker container."""
        self.treeWidget().command_docker_log(self)

    def command_docker_exec(self):
        """Exec a command on this docker container."""
        self.treeWidget().command_docker_exec(self)


class ECSElementsTreeWidget(QtWidgets.QTreeWidget):
    """Tree Widgets for all ECS elements."""

    sig_status_changed = QtCore.pyqtSignal(str)
    sig_command_show_detail = QtCore.pyqtSignal(QtWidgets.QTreeWidgetItem)
    sig_command_service_restart = QtCore.pyqtSignal(QtWidgets.QTreeWidgetItem)
    sig_command_service_show_events = QtCore.pyqtSignal(QtWidgets.QTreeWidgetItem)
    sig_command_task_stop = QtCore.pyqtSignal(QtWidgets.QTreeWidgetItem)
    sig_command_task_log = QtCore.pyqtSignal(QtWidgets.QTreeWidgetItem)
    sig_command_container_ssh = QtCore.pyqtSignal(QtWidgets.QTreeWidgetItem)
    sig_command_docker_log = QtCore.pyqtSignal(QtWidgets.QTreeWidgetItem)
    sig_command_docker_exec = QtCore.pyqtSignal(QtWidgets.QTreeWidgetItem)

    def __init__(self, parent=None):
        """Initialize tree widgets."""
        super(ECSElementsTreeWidget, self).__init__(parent)
        self.reload_cluster_info()
        self.currentItemChanged.connect(
            lambda item: self.show_status_on_selection(item)
        )
        self.itemActivated.connect(lambda item: item.refresh_children())
        self.itemDoubleClicked.connect(lambda item: item.refresh_children())

    def contextMenuEvent(self, event):
        """Open context menu depends on item options."""
        item = self.itemAt(event.pos())
        if item:
            menu = QtWidgets.QMenu(self)
            item.get_context_menu(menu)
            menu.exec_(event.globalPos())
        else:
            super(ECSElementsTreeWidget, self).contextMenuEvent(event)

    def keyPressEvent(self, e):
        """Process key pressed on this widget."""
        # if e.key() == QtCore.Qt.Key_Escape:
        #     self.close()

        super(ECSElementsTreeWidget, self).keyPressEvent(e)

    @QtCore.pyqtSlot()
    def reload_cluster_info(self):
        """Reload a list of clusters."""
        self.clear()
        for cluster in ecs_data.get_clusters():
            self.addTopLevelItem(ECSClusterTreeItem(cluster))

    def show_status_on_selection(self, item):
        """Update status bar with item info."""
        if item:
            self.sig_status_changed.emit(f"Selecting {item.name}: {item.identifier}")

    def command_show_detail(self, item):
        """Show attributes on detail view widget."""
        if item and isinstance(item, ECSTreeItem):
            self.sig_status_changed.emit(
                f"Show details for {item.name}: {item.identifier}"
            )
            self.sig_command_show_detail.emit(item)

    def command_service_restart(self, item):
        """Restart a service command."""
        if item and isinstance(item, ECSTreeItem):
            self.sig_status_changed.emit(
                f"Restarting service {item.name}: {item.identifier}"
            )
            self.sig_command_service_restart.emit(item)

    def command_task_stop(self, item):
        """Stop a task command."""
        if item and isinstance(item, ECSTreeItem):
            self.sig_status_changed.emit(
                f"Stopping task {item.name}: {item.identifier}"
            )
            self.sig_command_task_stop.emit(item)

    def command_task_log(self, item):
        """Show log of a task."""
        if item and isinstance(item, ECSTreeItem):
            self.sig_status_changed.emit(f"Log for task {item.name}: {item.identifier}")
            self.sig_command_task_log.emit(item)

    def command_container_ssh(self, item):
        """Access to container instance."""
        if item and isinstance(item, ECSTreeItem):
            self.sig_status_changed.emit(
                f"Access to ssh for {item.name}: {item.identifier}"
            )
            self.sig_command_container_ssh.emit(item)

    def command_docker_log(self, item):
        """Show log of docker container."""
        if item and isinstance(item, ECSTreeItem):
            self.sig_status_changed.emit(
                f"Docker log for {item.name}: {item.identifier}"
            )
            self.sig_command_docker_log.emit(item)

    def command_docker_exec(self, item):
        """Execute command on docker container."""
        if item and isinstance(item, ECSTreeItem):
            self.sig_status_changed.emit(
                f"Docker exec for {item.name}: {item.identifier}"
            )
            self.sig_command_docker_exec.emit(item)

    def command_service_show_events(self, item):
        """Show events of a service."""
        if item and isinstance(item, ECSTreeItem):
            self.sig_status_changed.emit(
                f"Show Events for {item.name}: {item.identifier}"
            )
            self.sig_command_service_show_events.emit(item)

    # @QtCore.pyqtSignal(str)
    # def operation_status(self, message):
    #     self.emit


class ECSAttributesTreeWidget(QtWidgets.QTreeWidget):
    """Widget to show item attributes."""

    sig_status_changed = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        """Initialize attributes view."""
        super(ECSAttributesTreeWidget, self).__init__(parent)
        self.currentItemChanged.connect(
            lambda item: self.show_status_on_selection(item)
        )

    def show_status_on_selection(self, item):
        """Update status bar on selection."""
        if item:
            self.sig_status_changed.emit(f"{item.text(0)}: {item.text(1)}")

    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem)
    def update_attributes(self, item):
        """Show a list of attributes of a selected ecs item."""
        self.clear()
        if item and isinstance(item, ECSTreeItem):
            for attr in item.get_attributes():
                self.addTopLevelItem(QtWidgets.QTreeWidgetItem([str(a) for a in attr]))


class ECSTabView(QtWidgets.QTabWidget):
    """Tab widgets for commands results."""

    def __init__(self, parent=None):
        """Initialize tab widget."""
        super(ECSTabView, self).__init__(parent)
        self.tabCloseRequested.connect(self.info_tab_closed)

    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem)
    def show_detail(self, item):
        """Show json info of a ecs element."""
        if item and item.detail and isinstance(item, ECSTreeItem):
            tab_id = self.addTab(ShowResult(pretty_json.dumps(item.detail)), item.name)
            self.setCurrentIndex(tab_id)

    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem)
    def container_ssh(self, item):
        """Open ssh terminal to access a container instance."""
        if item and item.detail and isinstance(item, ECSTreeItem):
            bash_command = ecs_ssh.ssh_cmd_container_instance(item.detail)
            tab_id = self.addTab(EmbTerminal(bash_command), item.name)
            self.setCurrentIndex(tab_id)

    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem)
    def service_events(self, item):
        """Show a list of events for a service."""
        if item and item.detail and isinstance(item, ECSServiceTreeItem):
            tab_id = self.addTab(
                ShowServiceEvents(item.detail["events"]), f"Events from {item.name}"
            )
            self.setCurrentIndex(tab_id)

    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem)
    def task_stop(self, item):
        """Send task stop command."""
        if item and item.detail and isinstance(item, ECSTaskTreeItem):
            question = QtWidgets.QMessageBox.question(
                self, f"Stopping {item.name}", f"Are you sure to stop {item.name}?"
            )
            if question == QtWidgets.QMessageBox.Yes:
                self.task_stop_ok(item)

    def task_stop_ok(self, item):
        """Show result of stop operation."""
        task_stopped = ecs_facade.stop_task(
            item.cluster_identifier, item.identifier, "Stopped from ECS Taks Operations"
        )
        tab_id = self.addTab(
            ShowResult(pretty_json.dumps(task_stopped)),
            f"Stopping {item.name}",
        )
        self.setCurrentIndex(tab_id)

    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem)
    def service_restart(self, item):
        """Restart a service."""
        if item and item.detail and isinstance(item, ECSServiceTreeItem):
            question = QtWidgets.QMessageBox.question(
                self,
                f"Restart {item.name}",
                f"Are you sure to force restart {item.name}?",
            )
            if question == QtWidgets.QMessageBox.Yes:
                self.service_restart_ok(item)

    def service_restart_ok(self, item):
        """Show result of restart a service."""
        service_restarted = ecs_facade.restart_service(
            item.cluster_identifier, item.identifier, True
        )
        tab_id = self.addTab(
            ShowResult(pretty_json.dumps(service_restarted)),
            f"Force Restart {item.name}",
        )
        self.setCurrentIndex(tab_id)

    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem)
    def task_log(self, item):
        """Open log terminal for a task (first docker container)."""
        if item and item.detail and isinstance(item, ECSTaskTreeItem):
            bash_command = ecs_ssh.ssh_cmd_task_log(item.detail)
            tab_id = self.addTab(EmbTerminal(bash_command), item.name)
            self.setCurrentIndex(tab_id)

    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem)
    def docker_container_log(self, item):
        """Open log terminal for a docker container."""
        if item and item.detail and isinstance(item, ECSDockerContainerTreeItem):
            bash_command = ecs_ssh.ssh_cmd_docker_container_log(item.detail)
            tab_id = self.addTab(EmbTerminal(bash_command), item.name)
            self.setCurrentIndex(tab_id)

    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem)
    def docker_container_exec(self, item):
        """Open terminal executing a command on docker container."""
        if item and item.detail and isinstance(item, ECSDockerContainerTreeItem):
            commands = ecs_conf.cfg.get("commands", ["/bin/sh"])
            command_on_docker, ok = QtWidgets.QInputDialog.getItem(
                self,
                "Command to execute on docker",
                "Command:",
                commands,
                editable=True,
            )
            if ok:
                bash_command = ecs_ssh.ssh_cmd_docker_container_exec(
                    item.detail, command_on_docker, True
                )
                tab_id = self.addTab(
                    EmbTerminal(bash_command), f"{command_on_docker} on {item.name}"
                )
                self.setCurrentIndex(tab_id)

    def info_tab_closed(self, index):
        """Close a tab."""
        self.widget(index).close()
        self.removeTab(index)


class ShowResult(QtWidgets.QWidget):
    """Show result widgets with text information."""

    def __init__(self, code_str, parent=None):
        """Initialize show result widget."""
        super(ShowResult, self).__init__(parent)

        layout = QtWidgets.QVBoxLayout()
        text = QtWidgets.QTextBrowser()
        text.setPlainText(code_str)
        layout.addWidget(text)

        self.setLayout(layout)


class EmbTerminal(QtWidgets.QWidget):
    """Open a embedded terminal widget."""

    def __init__(self, bash_command, parent=None):
        """Initilize parameters and open a terminal."""
        super(EmbTerminal, self).__init__(parent)
        self.process = QtCore.QProcess(self)
        self.terminal = QtWidgets.QWidget(self)
        self.command = QtWidgets.QLineEdit(self)
        self.command.setReadOnly(True)
        self.command.setText(bash_command)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.command)
        layout.addWidget(self.terminal)

        # env = QtCore.QProcessEnvironment.systemEnvironment()
        # env.insert("TERM", "xterm")
        # self.process.setProcessEnvironment(env)

        # Log errors
        # self.process.error.connect(self.log_error)

        # Works also with urxvt:
        terminal_args = []
        if bash_command:
            terminal_args = ["-e", "bash", "-c", bash_command] + terminal_args
        self.process.start(
            "urxvt", ["-embed", str(int(self.terminal.winId()))] + terminal_args
        )

    def closeEvent(self, event):
        """Close terminal and process."""
        self.process.terminate()

    def log_error(self, error):
        """Show log error information."""
        print(error)


class ShowServiceEvents(QtWidgets.QWidget):
    """Widget for a list of events."""

    def __init__(self, events, parent=None):
        """Initialize this widget for a list of events."""
        super(ShowServiceEvents, self).__init__(parent)

        layout = QtWidgets.QVBoxLayout(self)
        table = QtWidgets.QTableWidget(self)
        table.setRowCount(len(events))
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Date", "Message"])
        table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents
        )
        # table.horizontalHeader().setCascadingSectionResizes(True) # Only valid for QHeaderView.Interactive
        for row, e in enumerate(events):
            table.setItem(
                row,
                0,
                QtWidgets.QTableWidgetItem(
                    e["createdAt"].strftime("%Y-%m-%d %H:%M:%S")
                ),
            )
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(e["message"]))

        layout.addWidget(table)
        self.setLayout(layout)
