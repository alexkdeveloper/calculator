# window.py
#
# Copyright 2023 Alex
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import re

from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gio
from StringCalculator import SolveMathProblem

@Gtk.Template(resource_path='/io/github/alexkdeveloper/calculator/window.ui')
class CalculatorWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'CalculatorWindow'

    calculate_button = Gtk.Template.Child()
    entry = Gtk.Template.Child()
    text_view = Gtk.Template.Child()
    overlay = Gtk.Template.Child()

    text = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.calculate_button.connect("clicked", self.on_calculate_clicked)
        self.entry.connect("icon-press", self.on_clear_clicked)

        settings = Gio.Settings(schema_id="io.github.alexkdeveloper.calculator")

        settings.bind("width", self, "default-width", Gio.SettingsBindFlags.DEFAULT)
        settings.bind("height", self, "default-height", Gio.SettingsBindFlags.DEFAULT)
        settings.bind("is-maximized", self, "maximized", Gio.SettingsBindFlags.DEFAULT)
        settings.bind("is-fullscreen", self, "fullscreened", Gio.SettingsBindFlags.DEFAULT)

        event_controller = Gtk.EventControllerKey.new()
        event_controller.connect("key-released", self.on_key_released)

        self.add_controller(event_controller)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_string('.text_size {font-size: 16px;}')
        Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.entry.set_css_classes(["text_size"])
        self.text_view.set_css_classes(["text_size"])

    def on_key_released(self, event, keyval, keycode, state):
        if keyval == Gdk.KEY_Return or keyval == Gdk.KEY_KP_Enter:
           self.on_calculate_clicked(self)

    def on_calculate_clicked(self, widget):
        if len(self.entry.get_text().strip()) == 0:
           self.set_toast(_("Enter an arithmetic expression"))
           self.entry.grab_focus()
           return

        problem = re.sub(r"\s+", "", self.entry.get_text(), flags=re.UNICODE)

        try:
           result = SolveMathProblem(problem)
        except ZeroDivisionError:
             self.set_toast(_("Division by zero!"))
             self.entry.grab_focus()
             return

        self.text += problem + "=" + str(result) + "\n"

        self.text_view.get_buffer().set_text(self.text)

    def on_clear_clicked(self, widget, _):
        self.entry.set_text("")

    def set_toast(self, str):
        toast = Adw.Toast.new(str)
        toast.set_timeout(4)
        self.overlay.add_toast(toast)
