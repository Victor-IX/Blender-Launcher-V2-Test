from __future__ import annotations

from pathlib import Path

import pytest

import source.main as main
from source.windows.update_window import BlenderLauncherUpdater


def test_start_update_launches_updater_visible_on_windows(monkeypatch):
    calls: list[tuple[list[str], bool]] = []

    monkeypatch.setattr(main, "get_platform", lambda: "Windows")
    monkeypatch.setattr(main, "is_frozen", lambda: True)
    monkeypatch.setattr(main, "get_launcher_name", lambda: ("Blender Launcher.exe", "Blender Launcher Updater.exe"))
    monkeypatch.setattr(main, "get_cwd", lambda: Path("C:/Blender Launcher"))
    monkeypatch.setattr(main, "retry_on_permission_error", lambda *args, **kwargs: None)
    monkeypatch.setattr(main, "_popen", lambda args, no_console=True: calls.append((list(args), no_console)))

    with pytest.raises(SystemExit) as excinfo:
        main.start_update(app=object(), is_instanced=False, tag="v1.0.0")

    assert excinfo.value.code == 0
    assert calls == [(["Blender Launcher Updater.exe", "--instanced", "update"], False)]


def test_updater_finish_launches_launcher_visible_on_windows(monkeypatch, tmp_path):
    calls: list[tuple[list[str], bool]] = []

    monkeypatch.setattr(
        "source.windows.update_window._popen",
        lambda args, no_console=True: calls.append((list(args), no_console)),
    )

    class DummyApp:
        def __init__(self):
            self.quit_called = False

        def quit(self):
            self.quit_called = True

    class DummyUpdater:
        def __init__(self):
            self.platform = "Windows"
            self.app = DummyApp()
            self.source_zip = tmp_path / "update.zip"
            self.source_zip.write_text("zip")
            self.stopped = False

        def _stop_queue(self):
            self.stopped = True

    dummy = DummyUpdater()

    BlenderLauncherUpdater.finish(dummy, tmp_path / "Blender Launcher.exe", False)

    assert calls == [([str(tmp_path / "Blender Launcher.exe")], False)]
    assert dummy.stopped is True
    assert dummy.app.quit_called is True
