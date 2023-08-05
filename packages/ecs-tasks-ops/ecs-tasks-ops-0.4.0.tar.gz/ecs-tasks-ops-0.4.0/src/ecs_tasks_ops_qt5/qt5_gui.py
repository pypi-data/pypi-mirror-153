"""Qt5 User Interface for ECS Tasks Ops."""
import sys

import pkg_resources
from PyQt5 import QtWidgets

from ecs_tasks_ops import ecs_conf
from ecs_tasks_ops_qt5.about import UiAboutDialog
from ecs_tasks_ops_qt5.main_window import UiMainWindow


class AboutDialog(QtWidgets.QDialog, UiAboutDialog):
    """About Dialog widget."""

    def __init__(self, *args, **kwargs):
        """Initialize about dialog."""
        super(AboutDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)

        version = pkg_resources.get_distribution("ecs_tasks_ops").version
        self.version.setText(f"Version: {version}")


class MainWindow(QtWidgets.QMainWindow, UiMainWindow):
    """Main Window for this application."""

    def __init__(self, *args, obj=None, **kwargs):
        """Initialize application and connections between widgets."""
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.setWindowTitle("ECS Tasks Operations")

        self.splitter_horizontal.setSizes([100, 400])
        self.splitter_vertical.setSizes([200, 100])
        self.ecs_elements.sig_status_changed.connect(self.statusbar.showMessage)
        self.attributes.sig_status_changed.connect(self.statusbar.showMessage)

        self.action_quit.triggered.connect(self.close)
        self.action_about.triggered.connect(self.open_about)
        self.ecs_elements.currentItemChanged[
            "QTreeWidgetItem*", "QTreeWidgetItem*"
        ].connect(self.attributes.update_attributes)
        self.action_reload_clusters.triggered.connect(
            self.ecs_elements.reload_cluster_info
        )
        self.action_reload_config.triggered.connect(self.reload_conf)
        self.ecs_elements.sig_command_show_detail["QTreeWidgetItem*"].connect(
            self.tabWidget.show_detail
        )
        self.ecs_elements.sig_command_container_ssh["QTreeWidgetItem*"].connect(
            self.tabWidget.container_ssh
        )
        self.ecs_elements.sig_command_task_log["QTreeWidgetItem*"].connect(
            self.tabWidget.task_log
        )
        self.ecs_elements.sig_command_task_stop["QTreeWidgetItem*"].connect(
            self.tabWidget.task_stop
        )
        self.ecs_elements.sig_command_docker_log["QTreeWidgetItem*"].connect(
            self.tabWidget.docker_container_log
        )
        self.ecs_elements.sig_command_docker_exec["QTreeWidgetItem*"].connect(
            self.tabWidget.docker_container_exec
        )
        self.ecs_elements.sig_command_service_show_events["QTreeWidgetItem*"].connect(
            self.tabWidget.service_events
        )
        self.ecs_elements.sig_command_service_restart["QTreeWidgetItem*"].connect(
            self.tabWidget.service_restart
        )

    def open_about(self):
        """Open About Dialog widget."""
        about_dialog = AboutDialog(self)
        about_dialog.exec_()

    def reload_conf(self):
        """Reload configuration file."""
        ecs_conf.load_config()
        self.statusbar.showMessage("Reloading configuration")


def main_gui():
    """Main method to start QT5 application from cli."""
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main_gui()
