from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog
from PyQt6.QtCore import QCoreApplication
from .CompareThread import CompareThread
from .BrowseDialog import BrowseDialog
from .SettingsDialog import SettingsDialog
from .AboutDialog import AboutDialog
from PyQt6 import uic
import subprocess
import shutil
import sys
import os


class MainWindow(QMainWindow):
    def __init__(self, env):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "MainWindow.ui"), self)

        self._browse_dialog = BrowseDialog(env)
        self._settings_dialog = SettingsDialog(env)
        self._about_dialog = AboutDialog(env)

        self._compare_thread = CompareThread(env)
        self._compare_thread.finished.connect(self._compare_finished)

        self.action_compare_file.triggered.connect(self._compare_file_clicked)
        self.action_compare_directories.triggered.connect(self._compare_directory_clicked)
        self.action_reload.triggered.connect(self._compare_thread.start)
        self.action_exit.triggered.connect(lambda: sys.exit(0))

        self.action_settings.triggered.connect(self._settings_dialog.show_dialog)

        self.action_create_patch_file.triggered.connect(self._create_patch_file_clicked)

        self.action_about.triggered.connect(self._about_dialog.exec)
        self.action_about_qt.triggered.connect(QApplication.instance().aboutQt)

        self.tree_files.itemDoubleClicked.connect(self._tree_files_item_double_click)

        self.edit_diff_original.verticalScrollBar().valueChanged.connect(lambda position: self.edit_diff_copy.verticalScrollBar().setSliderPosition(position))
        self.edit_diff_copy.verticalScrollBar().valueChanged.connect(lambda position: self.edit_diff_original.verticalScrollBar().setSliderPosition(position))

    def _compare_file_clicked(self):
        files = self._browse_dialog.get_files()

        if not files:
            return

        self._compare_thread.setup(files[0], files[1])
        self._compare_thread.start()

        self.action_reload.setEnabled(True)

    def _compare_directory_clicked(self):
        directories = self._browse_dialog.get_directories()

        if not directories:
            return

        self._compare_thread.setup(directories[0], directories[1])
        self._compare_thread.start()

        self.action_reload.setEnabled(True)

    def _compare_finished(self):
        self.tree_files.takeTopLevelItem(0)
        self.tree_files.addTopLevelItem(self._compare_thread.get_root_item())
        self.action_create_patch_file.setEnabled(True)

        self.statusBar().showMessage(QCoreApplication.translate("MainWindow", "diff finished"), 3000)

    def _create_patch_file_clicked(self):
        if not shutil.which("diff"):
            QMessageBox.critical(self, QCoreApplication.translate("MainWindow", "diff not found"), QCoreApplication.translate("MainWindow", "diff was not found. Make sure it is installed and in PATH."))
            return

        path = QFileDialog.getSaveFileName(self, filter="Patch (*.patch);;All Files (*)")

        if path[0] == "":
            return

        original_path = self._compare_thread.get_original_path()
        copy_path = self._compare_thread.get_copy_path()

        result = subprocess.run(["diff", "-ruN", original_path, copy_path], capture_output=True, text=True)

        # https://stackoverflow.com/questions/6971284/what-are-the-error-exit-values-for-diff
        if result.returncode >= 2:
            QMessageBox.critical(self, QCoreApplication.translate("MainWindow", "Error"), QCoreApplication.translate("MainWindow", "An unknown error occurred"))
            return

        with open(path[0], "w", encoding="utf-8") as f:
            f.write(result.stdout)

        self.statusBar().showMessage(QCoreApplication.translate("MainWindow", "{{path}} created").replace("{{path}}", path[0]), 3000)

    def _tree_files_item_double_click(self, item):
        self.edit_diff_original.setHtml(item.original_html)
        self.edit_diff_copy.setHtml(item.copy_html)
