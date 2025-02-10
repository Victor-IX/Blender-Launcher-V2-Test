from modules.settings import (
    get_scrape_automated_builds,
    get_scrape_bfa_builds,
    get_scrape_stable_builds,
    get_show_bfa_builds,
    get_show_daily_builds,
    get_show_experimental_and_patch_builds,
    get_show_stable_builds,
)
from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QSizePolicy,
    QVBoxLayout,
)
from widgets.repo_visibility_view import RepoUserView


class RepoGroup(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProperty("SettingsGroup", True)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.stable_repo = RepoUserView(
            "Stable",
            "Production-ready builds.",
            library=get_show_stable_builds(),
            download=get_scrape_stable_builds(),
            parent=self,
        )
        self.daily_repo = RepoUserView(
            "Daily",
            "Builds created every day. They have the latest features and bug fixes, but they can be unstable.",
            library=get_show_daily_builds(),
            download=get_scrape_automated_builds(),
            bind_download_to_library=False,
            parent=self,
        )
        self.experimental_repo = RepoUserView(
            "Experimental and Patch",
            "These have new features that may end up in official Blender releases. They can be unstable.",
            library=get_show_experimental_and_patch_builds(),
            download=get_scrape_automated_builds(),
            bind_download_to_library=False,
            parent=self,
        )
        self.bforartists_repo = RepoUserView(
            "Bforartists",
            "A popular fork of Blender with the goal of improving the UI.",
            library=get_show_bfa_builds(),
            download=get_scrape_bfa_builds(),
            parent=self,
        )

        self.daily_repo.library_changed.connect(self.check_if_both_automated_are_disabled)
        self.experimental_repo.library_changed.connect(self.check_if_both_automated_are_disabled)

        self.automated_groups = QButtonGroup()
        self.automated_groups.setExclusive(False)
        self.daily_repo.add_downloads_to_group(self.automated_groups)
        self.experimental_repo.add_downloads_to_group(self.automated_groups)

        self.check_if_both_automated_are_disabled()

        self.repos = [
            self.stable_repo,
            self.daily_repo,
            self.experimental_repo,
            self.bforartists_repo,
        ]

        self.layout_ = QVBoxLayout(self)
        self.layout_.setContentsMargins(0, 0, 0, 5)

        for widget in self.repos:
            self.layout_.addWidget(widget)

    @Slot()
    def check_if_both_automated_are_disabled(self):
        if (not self.daily_repo.library) and (not self.experimental_repo.library):
            self.daily_repo.download = False  # Will also set experimental_repo
            self.daily_repo.download_enable_button.setEnabled(False)
            self.experimental_repo.download_enable_button.setEnabled(False)
            return
        if (self.daily_repo.library or self.experimental_repo.library) and not self.daily_repo.download:
            self.daily_repo.download_enable_button.setEnabled(True)
            self.experimental_repo.download_enable_button.setEnabled(True)

    def total_height(self):
        return sum(r.height() for r in self.repos)
