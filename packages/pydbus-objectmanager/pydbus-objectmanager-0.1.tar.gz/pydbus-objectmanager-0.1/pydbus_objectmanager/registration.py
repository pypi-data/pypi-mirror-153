# -*- coding: utf-8 -*-

from __future__ import print_function

from gi.repository import Gio
from pydbus import Variant
from pydbus.generic import signal

class RegistrationMixin:
	_objects = {}

	InterfacesAdded = signal()
	InterfacesRemoved = signal()

	def _add_object(self, path, object, node_info=None):
		if node_info is None:
			try:
				node_info = type(object).dbus
			except AttributeError:
				node_info = type(object).__doc__

		self._objects[(path, object)] = node_info

		interfaces_and_properties = self._get_interfaces_and_properties(path, object)
		self.InterfacesAdded(path, interfaces_and_properties)

	def _remove_object(self, path, object):
		node_info = self._objects.pop((path, object))
		node_info = Gio.DBusNodeInfo.new_for_xml(node_info)
		interfaces = [iface.name for iface in node_info.interfaces]
		self.InterfacesRemoved(path, interfaces)

	def _get_interfaces_and_properties(self, path, object):
		node_info = self._objects.get((path, object))
		node_info = Gio.DBusNodeInfo.new_for_xml(node_info)
		interfaces = node_info.interfaces

		interfaces_and_properties = {}
		for iface in interfaces:
			interfaces_and_properties[iface.name] = {}

			for prop in iface.properties:
				try:
					value = getattr(object, prop.name)
					variant = Variant(prop.signature, value)

					interfaces_and_properties[iface.name][prop.name] = variant
				except:
					pass

		return interfaces_and_properties

	def register_object(self, path, object, node_info):
		"""Register object on the bus."""
		manager = self
		bus = self.bus

		registration = bus.register_object(path, object, node_info)

		# signals
		manager._add_object(path, object, node_info)
		registration._at_exit(lambda *args: manager._remove_object(path, object))

		return registration

	def GetManagedObjects(self):
		"""Implementation of org.freedesktop.DBus.ObjectManager.GetManagedObjects()"""
		object_paths_interfaces_and_properties = {}

		for path, object in self._objects.keys():
			interfaces_and_properties = self._get_interfaces_and_properties(path, object)
			if path not in object_paths_interfaces_and_properties:
				object_paths_interfaces_and_properties[path] = interfaces_and_properties
			else:
				object_paths_interfaces_and_properties[path].update(interfaces_and_properties)

		return object_paths_interfaces_and_properties
