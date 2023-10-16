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

from gi.repository import Adw
from gi.repository import Gtk
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

        self.settings = Gio.Settings(schema_id="io.github.alexkdeveloper.calculator")

        self.settings.bind("width", self, "default-width", Gio.SettingsBindFlags.DEFAULT)
        self.settings.bind("height", self, "default-height", Gio.SettingsBindFlags.DEFAULT)
        self.settings.bind("is-maximized", self, "maximized", Gio.SettingsBindFlags.DEFAULT)
        self.settings.bind("is-fullscreen", self, "fullscreened", Gio.SettingsBindFlags.DEFAULT)

    def on_calculate_clicked(self, widget):
        if len(self.entry.get_text().strip()) == 0:
           self.set_toast(_("Enter an arithmetic expression"))
           return

        problem = self.entry.get_text()

        try:
           result = SolveMathProblem(problem)
        except ZeroDivisionError:
             self.set_toast(_("Division by zero!"))
             return

        self.text += problem + "=" + str(result) + "\n"

        self.text_view.get_buffer().set_text(self.text)

    def on_clear_clicked(self, widget, _):
        self.entry.set_text("")

    def set_toast(self, str):
        toast = Adw.Toast.new(str)
        toast.set_timeout(4)
        self.overlay.add_toast(toast)