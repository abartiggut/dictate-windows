"""Regression checks without microphone capture or keyboard injection."""
import os
os.environ["QT_QPA_PLATFORM"] = "offscreen"

import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import core
import gui
import setup_windows


class Suppressed(Exception):
    pass


class FakeListener:
    def __init__(self, **kwargs):
        self.options = kwargs

    def start(self):
        pass

    def suppress_event(self):
        raise Suppressed


class ImmediateThread:
    def __init__(self, target, args=(), **kwargs):
        self.target, self.args = target, args

    def start(self):
        self.target(*self.args)


@unittest.skipUnless(sys.platform == "win32", "Windows keyboard hook")
class HotkeyTests(unittest.TestCase):
    def test_only_selected_function_key_is_captured(self):
        pressed, released = [], []
        with patch.object(gui.keyboard, "Listener", FakeListener):
            listener = gui._make_listener(
                pressed.append, released.append, {gui.keyboard.Key.f9}
            )
        event_filter = listener.options["win32_event_filter"]
        for msg in (0x0100, 0x0101):
            with self.assertRaises(Suppressed):
                event_filter(msg, SimpleNamespace(vkCode=gui.keyboard.Key.f9.value.vk))
        self.assertEqual(pressed, [gui.keyboard.Key.f9])
        self.assertEqual(released, [gui.keyboard.Key.f9])
        for key_code in (0x41, 0x0D, 0x11, 0x77):
            self.assertTrue(event_filter(0x0100, SimpleNamespace(vkCode=key_code)))
        self.assertEqual(pressed, [gui.keyboard.Key.f9])
        self.assertEqual(released, [gui.keyboard.Key.f9])


class InsertionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = gui.QApplication.instance() or gui.QApplication([])

    def setUp(self):
        with patch.object(gui.MainWindow, "start_listener"), \
             patch.object(gui.MainWindow, "_preload_local_if_needed"), \
             patch.object(core, "provider_key", return_value="installed"), \
             patch.object(gui.QSystemTrayIcon, "isSystemTrayAvailable", return_value=False):
            self.win = gui.MainWindow()

    def tearDown(self):
        self.win.deleteLater()
        self.app.processEvents()

    def test_own_window_displays_text_without_typing_or_opening_settings(self):
        with patch.object(gui.QApplication, "activeWindow", return_value=self.win), \
             patch.object(core, "type_text") as type_text, \
             patch.object(self.win, "open_settings") as settings:
            self.win.on_transcribed("Hallo Codex, eine Nachricht mit Leerzeichen.")
            type_text.assert_not_called()
            settings.assert_not_called()
            self.assertEqual(self.win.last.toPlainText(), "Hallo Codex, eine Nachricht mit Leerzeichen.")
            self.assertTrue(self.win.copy_btn.isEnabled())

    def test_external_target_receives_text(self):
        with patch.object(gui.QApplication, "activeWindow", return_value=None), \
             patch.object(gui.threading, "Thread", ImmediateThread), \
             patch.object(core, "type_text") as type_text:
            self.win.on_transcribed("Nachricht an das externe Eingabefeld.")
            type_text.assert_called_once_with("Nachricht an das externe Eingabefeld.")

    def test_copy_button_copies_transcription(self):
        self.win.last.setPlainText("Deutsch mit Umlauten: äöü.")
        self.win.copy_transcription()
        self.assertEqual(self.app.clipboard().text(), "Deutsch mit Umlauten: äöü.")


class SetupTests(unittest.TestCase):
    def test_new_configuration_uses_local_model(self):
        with tempfile.TemporaryDirectory() as folder:
            config_dir = Path(folder)
            with patch.multiple(core, CONFIG_DIR=config_dir, CONFIG_PATH=config_dir / "config.json"):
                self.assertTrue(setup_windows.configure_local_defaults())
                cfg = core.load_config()
                self.assertEqual(cfg["provider"], "parakeet_local")
                self.assertEqual(cfg["key"], "f9")
                self.assertEqual(cfg["openai_api_key"], "")

    def test_existing_configuration_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as folder:
            config_dir = Path(folder)
            config_path = config_dir / "config.json"
            contents = b'{"provider":"yorik","key":"f8","yorik_token":"test-placeholder"}'
            config_path.write_bytes(contents)
            with patch.multiple(core, CONFIG_DIR=config_dir, CONFIG_PATH=config_path):
                self.assertFalse(setup_windows.configure_local_defaults())
                self.assertEqual(config_path.read_bytes(), contents)


if __name__ == "__main__":
    unittest.main()
