#!/usr/bin/env python3
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# main.py
# Copyright (C) 2021 Reuben <silrep@emypeople.net>
# 
# motor_speed_resistor is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# motor_speed_resistor is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import os, sys


UI_FILE = "src/open_electronic_workbench.ui"


class GUI(Gtk.Builder):
	def __init__(self):

		Gtk.Builder.__init__(self)
		self.add_from_file(UI_FILE)
		self.connect_signals(self)

		window = self.get_object('window')
		window.show_all()

	def on_window_destroy(self, window):
		Gtk.main_quit()

	def spinbutton_focus_in (self, widget, event):
		GLib.idle_add(widget.select_region, 0, -1)

	def calculate_steps_clicked (self, button):
		store = self.get_object('liststore1')
		store.clear()
		voltage = self.get_object('voltage_spinbutton').get_value()
		current = self.get_object('current_spinbutton').get_value()
		steps = self.get_object('steps_spinbutton').get_value_as_int()
		for i in range(1, steps + 1):
			motor_voltage = voltage / steps * i
			step_current = current / steps * i
			resistor_ohms = (voltage - motor_voltage) / step_current
			resistor_voltage = voltage - motor_voltage
			resistor_watts = resistor_voltage * step_current
			store.append([i, 
							motor_voltage, 
							step_current, 
							resistor_voltage,
							step_current,
							resistor_ohms, 
							resistor_watts])

	def voltage_checkbutton_toggled (self, togglebutton):
		active = not togglebutton.get_active()
		self.get_object('voltage_spinbutton').set_sensitive(active)

	def current_checkbutton_toggled (self, togglebutton):
		active = not togglebutton.get_active()
		self.get_object('current_spinbutton').set_sensitive(active)

	def ohm_checkbutton_toggled (self, togglebutton):
		active = not togglebutton.get_active()
		self.get_object('ohm_spinbutton').set_sensitive(active)

	def voltage_value_changed (self, spinbutton):
		self.calculate_parameters ()

	def current_value_changed (self, spinbutton):
		self.calculate_parameters ()

	def ohm_value_changed (self, spinbutton):
		self.calculate_parameters ()

	def calculate_parameters (self):
		if self.get_object('voltage_priority_button').get_active():
			ohms = self.get_object('ohm_spinbutton').get_value()
			current = self.get_object('current_spinbutton').get_value()
			self.get_object('voltage_spinbutton').set_value(ohms * current)
		if self.get_object('current_priority_button').get_active():
			voltage = self.get_object('voltage_spinbutton').get_value()
			ohms = self.get_object('ohm_spinbutton').get_value()
			self.get_object('current_spinbutton').set_value(voltage / ohms)
		if self.get_object('ohm_priority_button').get_active():
			voltage = self.get_object('voltage_spinbutton').get_value()
			current = self.get_object('current_spinbutton').get_value()
			self.get_object('ohm_spinbutton').set_value(voltage / current)

def main():
	app = GUI()
	Gtk.main()
		
if __name__ == "__main__":
	sys.exit(main())

