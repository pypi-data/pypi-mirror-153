# File: /gtklara/__init__.py
# Project: gtklara
# File Created: 06-06-2022 11:22:37
# Author: Clay Risser
# -----
# Last Modified: 06-06-2022 12:02:57
# Modified By: Clay Risser
# -----
# Risser Labs LLC (c) Copyright 2022
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import gi
from .state import State

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class GTKlara:
    ignore_signals = []
    ignore_methods = []
    ignore_values = []
    prop_bindings = {}
    signal_bindings = {}
    __cleanup = []

    def __init__(self, children=[], props={}, file_path=None):
        self._ready = False
        self._active = None
        self._edges = []
        self._builder = None
        self._props = props
        self.__signal_bindings_set = set(
            map(lambda key: "on_" + key, self.signal_bindings.keys())
        )
        self.__children = self.__get_children(children)
        if file_path:
            builder = Gtk.Builder()
            dir_path = os.path.dirname(os.path.realpath(file_path))
            name = file_path[len(dir_path) + 1 : len(file_path) - 3]
            builder.add_objects_from_file(
                os.path.join(dir_path, name + ".glade"),
                ("root", ""),
            )
            self._builder = builder
            self._root = builder.get_object("root")
            active = builder.get_object("active")
            self._active = active if active else self._root
            self._edges = self.__get_edges()
            self.__proxy_active_methods_and_values()
            self.__register_active_signals()
            self.__register_prop_bindings()
            self.__register_signal_bindings()
        else:
            self._root = self.render()._root
        self._ready = True
        self._render()

    @property
    def Children(self):
        return Children(self.__children)

    @property
    def _children(self):
        return self.__unpack_children(self.__children)

    def destroy(self):
        for cb in self.__cleanup:
            cb()
        if hasattr(self, "unmount"):
            self.unmount()

    def add(self, children):
        for edge in self._edges:
            self._add(edge, children)

    def clear(self):
        for edge in self._edges:
            self._clear(edge)

    def _get(self, id):
        if isinstance(id, GTKlara):
            return id._root
        return self._builder.get_object(id) if type(id) is str else id

    def _add(self, id, children):
        children = self.__unpack_children(children)
        for child in children:
            if child is None:
                continue
            widget = self._get(id)
            if hasattr(widget, "add") and callable(widget.add):
                widget.add(self._get(child))

    def _clear(self, id):
        widget = self._get(id)
        for child in widget.get_children():
            widget.remove(child)

    def _remove(self, id, child):
        self._get(id).remove(child)

    def _render(self):
        self.clear()
        for child in self.__unpack_children():
            self.add(child)

    def _prop(self, name):
        return self._get_value(self._props[name]) if name in self._props else None

    def _get_value(self, value):
        if isinstance(value, State):
            return value.get()
        return value

    def _set_value(self, name, value, id=None):
        if not id:
            id = self._active
        if not id:
            return
        setter_name = name if name[0:4] == "set_" else "set_" + name
        widget = self._get(id)
        if isinstance(value, State):
            setter = getattr(widget, setter_name)
            self.__cleanup.append(value.bind(setter))
            return
        getattr(widget, setter_name)(value)

    def _set_signal(self, name, value, id=None):
        if not id:
            id = self._active
        if not id:
            return
        signal_name = name[3:] if name[0:3] == "on_" else name
        prop_name = "on_" + signal_name
        widget = self._get(id)
        if isinstance(value, State):

            handler_id = None

            def handler(value):
                global handler_id
                handler_id = widget.connect(signal_name, value)

            unbind = value.bind(handler)

            def cleanup():
                if handler_id:
                    widget.disconnect(handler_id)
                unbind()

            self.__cleanup.append(cleanup)
            return
        if prop_name in self._props:
            widget.connect(signal_name, self._props[prop_name])

    def __get_children(self, children):
        if isinstance(children, Children):
            if isinstance(children.children, State):

                def handler(value):
                    if self._ready:
                        self._render()

                children.children.bind(handler)
        if children is None:
            return []
        elif isinstance(children, State):
            return children
        else:
            return children if type(children) is list else [children]

    def __unpack_children(self, children=None):
        if not children:
            children = self.__children
        if not children:
            return []
        if isinstance(children, Children):
            children = children.children
        children = self._get_value(children)
        return children if type(children) is list else [children]

    def __get_edges(self, edges=None):
        if not edges or len(edges) <= 0:
            edges = []
            edge = self._builder.get_object("edge")
            edge0 = self._builder.get_object("edge0")
            if not edge and not edge0:
                return edges
            if edge:
                edges.append(edge)
            if edge0:
                edges.append(edge0)
            return self.__get_edges(edges)
        edge = self._builder.get_object("edge" + str(len(edges)))
        if not edge:
            return edges
        edges.append(edge)
        return self.__get_edges(edges)

    def __register_active_signals(self):
        active = self._active
        if self.ignore_signals == True:
            return
        ignore_signals = set(self.ignore_signals)
        for key, value in self._props.items():
            if key[0:3] == "on_":
                signal_name = key[3:]
                if (
                    signal_name not in ignore_signals
                    and signal_name not in self.signal_bindings
                ):
                    try:
                        self._set_signal(signal_name, value)
                    except Exception as e:
                        if str(e).index("unknown signal name: " + signal_name) <= -1:
                            raise e

    def __register_prop_bindings(self):
        active = self._active
        for prop_name, binding in self.prop_bindings.items():
            if prop_name in self._props:
                arr = binding.split(":")
                value_name = arr.pop()
                id = ":".join(arr) if len(arr) > 0 else active
                self._set_value(value_name, self._props[prop_name], id)

    def __register_signal_bindings(self):
        active = self._active
        for signal_name, binding in self.signal_bindings.items():
            prop_name = "on_" + signal_name
            if prop_name in self._props:
                arr = binding.split(":")
                signal_name = arr.pop()
                id = ":".join(arr) if len(arr) > 0 else active
                self._set_signal(signal_name, self._props[prop_name], id)

    def __proxy_active_methods_and_values(self):
        active = self._active
        if self.ignore_methods is True and self.ignore_values is True:
            return
        ignore_methods = set(
            self.ignore_methods if type(self.ignore_methods) is list else []
        )
        ignore_values = set(
            self.ignore_methods if type(self.ignore_values) is list else []
        )
        for base in active.__class__.__bases__:
            for method in dir(base):
                if (
                    len(method) > 0
                    and method[0] != "_"
                    and method not in set(dir(self))
                    and method not in self.prop_bindings
                    and method not in self.__signal_bindings_set
                    and callable(getattr(base, method))
                ):
                    if (
                        len(method) > 4
                        and method[0:4] == "set_"
                        and ignore_values is not True
                    ):
                        value_name = method[4:]
                        if (
                            value_name not in ignore_values
                            and value_name in self._props
                        ):
                            self._set_value(method, self._props[value_name])
                    elif ignore_methods is not True and method not in ignore_methods:
                        setattr(self, method, getattr(active, method))


class Children:
    def __init__(self, children):
        self.children = children
